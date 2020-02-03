import logging
from decimal import Decimal
from datetime import datetime

from flask import request
from marshmallow import ValidationError
from flask_restplus import Namespace, Resource, fields

from app.lib import errors
from app.database import session_scope
from app.schemas import AccountSchema, AccountCreationSchema, \
    AccountUpdateSchema, TradeSchema
from app.models import Account, Stock, Trade
from app.resources.base_resource import BaseResource
from app.services.third_party.wtd import WorldTradingData

accounts_ns = Namespace('accounts', description='Account API Functions')

@accounts_ns.doc()
class AccountResource(BaseResource):
    def get(self, id):
        """
        Get account information such as cash and equity totals, as well as
        list of currently held stock positions.

        Params
        ------
        id : int
            Account identifier.
        """
        try:
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)

                stocks = {}
                for stock in account.stocks:
                    stocks[stock.symbol] = {
                        'id': stock.id, 
                        'symbol': stock.symbol, 
                        'shares': stock.number_of_shares,
                        'bought_at': stock.bought_at
                    }

                stock_list = stocks.keys()
                if len(stock_list) > 0:
                    ex = WorldTradingData().get_stocks(stock_list)
                    stock_data = ex['data']
                    for stock in stock_data:
                        if stock['symbol'] in stocks:
                            stocks[stock['symbol']]['price'] = float(stock['price'])

                schema = AccountSchema()
                data = schema.dump(account)
                data['stocks'] = stocks
        except Exception as e:
            logging.error(str(e))
            return self.error_response(errors.DEFAULT)

        return self.success_response(data)

    def patch(self, id, action):
        """
        Update the amount of available "cash" in the specified account.

        Params
        ------
        id : int
            Account identifier.
        action : str
            'withdraw' or 'deposit'
        """
        try:
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)

                schema = AccountUpdateSchema()
                data = schema.loads(request.get_data())
                if action == 'deposit':
                    account.cash_amount += data['amount']
                elif action == 'withdraw':
                    account.cash_amount -= data['amount']
        except Exception as e:
            logging.error(str(e))
            return self.error_response(errors.DEFAULT)
        
        return self.success_response(result='ok')
    
    def post(self):
        """
        Create a new account to associate with specified user.
        """
        created_account_id = None
        schema = AccountCreationSchema()
        try:
            data = schema.loads(request.get_data())
            with session_scope() as session:
                account = session.query(Account).filter_by(user_id=data['user_id']).first()
                if account:
                    return self.error_response(errors.ACCOUNT_EXISTS, self.HTTP_BAD_REQUEST)
                
                account = Account(**data)
                session.add(account)
                session.flush()

                created_account_id = account.id
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(errors.DEFAULT)
        
        return self.success_response(result={'id': created_account_id}, status_code=self.HTTP_CREATED)

    def delete(self, id):
        """
        Delete the specified brokerage account.

        Params
        ------
        id : int
            Account identifier.
        """
        try:
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)
                account.delete()
        except Exception as err:
            logging.error(str(err))
            return self.error_response(errors.DEFAULT)
        return self.success_response(result='ok')

@accounts_ns.doc()
class StockResource(BaseResource):
    def put(self, id, stock_id):
        """
        Trade (buy or sell) more of the specified stock.

        Params
        ------
        id : int
            Account identifier.
        stock_id : int
            Account stock identifier.
        """
        result = {}
        try:
            with session_scope() as session:
                account = session.query(Account).\
                    join(Account.stocks).\
                    filter(Account.id == id, Stock.id == stock_id).first()

                if not account:
                    return self.error_response(errors.STOCK_DNE, self.HTTP_NOT_FOUND)

                schema = TradeSchema()
                data = schema.loads(request.get_data())

                stock = account.stocks[0]
                if data['trade_type'] == 'buy':
                    cost = data['amount'] + Account.BROKERAGE_FEE
                    if account.cash_amount < cost:
                        return self.success_response(result=errors.NOT_ENOUGH_FUNDS, success=False)
                    stock.shares += data['shares']
                    account.cash_amount -= cost
                    account.equity_amount += data['amount']
                elif data['trade_type'] == 'sell':
                    if account.cash_amount < Account.BROKERAGE_FEE:
                        return self.success_response(result=errors.NOT_ENOUGH_FUNDS, success=False)
                    if stock.shares < data['shares']:
                        return self.success_response(result=errors.TOO_MANY_SHARES, success=False)
                    if stock.shares == data['shares']:
                        stock.sold_on = datetime.now
                    stock.shares -= data['shares']
                    account.cash_amount -= Account.BROKERAGE_FEE
                    account.cash_amount += data['amount']
                    account.equity_amount -= data['amount']

                trade = Trade(
                    user_id=account.user_id,
                    account_id=account.id,
                    stock_id=stock.id,
                    trade_type=data['trade_type'],
                    symbol=data['symbol'],
                    price=data['price'],
                    shares=data['shares'],
                )
                session.add(trade)
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(errors.DEFAULT)
        return self.success_response('ok')

    def post(self, id):
        """
        Buy a stock with given `symbol`, `shares` and `price`.

        Params
        ------
        id : int
            Account identifier.
        """
        try:
            result = {}

            schema = TradeSchema()
            data = schema.loads(request.get_data())
            data['account_id'] = id
            trade_type = 'buy'
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)

                total = data['amount'] + Account.BROKERAGE_FEE
                if account.cash_amount < total:
                    return self.success_response(result=errors.NOT_ENOUGH_FUNDS, success=False)

                existing_s = session.query(Stock).filter_by(account_id=id, symbol=data['symbol']).first()
                if existing_s:
                    return self.error_response(errors.STOCK_EXISTS, self.HTTP_BAD_REQUEST)

                s = Stock(
                    account_id=id,
                    bought_at=data['price'],
                    bought_on=data['process_date'],
                    initial_cost=data['amount'],
                    shares=data['shares'],
                    symbol=data['symbol']
                )
                session.add(s)
                session.flush()

                s_id = s.id
                if s_id:
                    account.cash_amount -= Account.BROKERAGE_FEE
                    account.cash_amount -= total
                    account.equity_amount += data['amount']
                    result['id'] = s_id
                    result['account'] = {'cash': account.cash_amount, 'equity': account.equity_amount}

                trade = Trade(
                    user_id=account.user_id,
                    account_id=account.id,
                    stock_id=s_id,
                    trade_type=trade_type,
                    symbol=data['symbol'],
                    price=data['price'],
                    shares=data['shares'],
                )
                session.add(trade)
        except ValidationError as err:
            return self.error_response(err.messages, self.HTTP_BAD_REQUEST)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(errors.DEFAULT)
        return self.success_response(result=result, status_code=self.HTTP_CREATED)

accounts_ns.add_resource(AccountResource, '', methods=['POST'])
accounts_ns.add_resource(AccountResource, '/<id>', methods=['GET', 'DELETE'])
accounts_ns.add_resource(AccountResource, '/<id>/withdraw', '/<id>/deposit', methods=['PATCH'])
accounts_ns.add_resource(StockResource, '/<id>/stocks', methods=['POST'])
accounts_ns.add_resource(StockResource, '/<id>/stocks/<stock_id>', methods=['PUT'])