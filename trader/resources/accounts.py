import logging
from decimal import Decimal
from datetime import datetime

from flask import request
from marshmallow import ValidationError
from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, fields

from trader.lib import errors
from trader.extensions import db
from trader.schemas import AccountReadSchema, AccountCreationSchema, \
    AccountUpdateSchema, TradeSchema
from trader.models import Account, Stock, Trade
from trader.resources.base_resource import BaseResource, validate_request_json
from trader.services.third_party.wtd import WorldTradingData

accounts_ns = Namespace('accounts', description='Account API Functions')

@accounts_ns.doc()
class AccountResource(BaseResource):
    @login_required
    def get(self):
        """
        Get account information such as cash and equity totals, as well as
        list of currently held stock positions.

        Params
        ------
        id : int
            Account identifier.
        """
        with db.session_scope() as session:
            account = session.query(Account).filter_by(user_id=current_user.id).first()
            if not account:
                return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)

            stocks = {}
            for stock in account.stocks:
                stocks[stock.symbol] = {
                    'id': stock.id, 
                    'symbol': stock.symbol, 
                    'shares': stock.shares,
                    'bought_at': format(stock.bought_at, '.2f')
                }

            stock_list = stocks.keys()
            if len(stock_list) > 0:
                ex = WorldTradingData().get_stocks(stock_list)
                stock_data = ex['data']
                for stock in stock_data:
                    if stock['symbol'] in stocks:
                        stocks[stock['symbol']]['price'] = format(float(stock['price']), '.2f')

            schema = AccountReadSchema()
            data = schema.dump(account)
            data['stocks'] = stocks

        return self.success_response(data)

    @login_required
    @validate_request_json
    def patch(self, action):
        """
        Update the amount of available "cash" in the specified account.

        Params
        ------
        id : int
            Account identifier.
        action : str
            'withdraw' or 'deposit'
        """
        if action not in ['withdraw', 'deposit']:
            return self.error_response(errors.ACCOUNT_INVALID_ACTION, self.HTTP_BAD_REQUEST)

        with db.session_scope() as session:
            account = session.query(Account).filter_by(id=current_user.id).first()
            if not account:
                return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)

            schema = AccountUpdateSchema()
            try:
                data = schema.loads(request.get_data())
            except ValidationError as err:
                return self.error_response(err.messages)
            
            if action == 'deposit':
                account.cash_amount += data['amount']
            elif action == 'withdraw':
                account.cash_amount -= data['amount']
        
        return self.success_response(result='ok')
    
    @login_required
    @validate_request_json
    def post(self):
        """
        Create a new account to associate with specified user.
        """
        created_account_id = None
        schema = AccountCreationSchema()
        try:
            data = schema.loads(request.get_data())
        except ValidationError as err:
            return self.error_response(err.messages)
        
        with db.session_scope() as session:
            account = session.query(Account).filter_by(user_id=current_user.id).first()
            if account:
                return self.error_response(errors.ACCOUNT_EXISTS, self.HTTP_BAD_REQUEST)
            
            data['user_id'] = current_user.id

            account = Account(**data)
            session.add(account)
            session.flush()

            created_account_id = account.id

        return self.success_response(result={'id': created_account_id}, status_code=self.HTTP_CREATED)

    @login_required
    def delete(self):
        """
        Delete the specified brokerage account.

        Params
        ------
        id : int
            Account identifier.
        """
        with db.session_scope() as session:
            account = session.query(Account).filter_by(id=current_user.id)
            if not account:
                return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)
            account.delete()
        return self.success_response(result='ok')

@accounts_ns.doc()
class StockResource(BaseResource):
    @validate_request_json
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
        schema = TradeSchema()
        try:
            data = schema.loads(request.get_data())
        except ValidationError as err:
            return self.error_response(err.messages)
        
        with db.session_scope() as session:
            account = session.query(Account).\
                join(Account.stocks).\
                filter(Account.id == id, Stock.id == stock_id, Stock.symbol == data['symbol']).first()

            if not account:
                return self.error_response(errors.STOCK_DNE, self.HTTP_NOT_FOUND)
            
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
                    stock.sold_on = data['process_date']
                stock.shares -= data['shares']
                account.cash_amount -= Account.BROKERAGE_FEE
                account.cash_amount += data['amount']
                account.equity_amount -= data['amount']

            trade = Trade(
                user_id=account.user_id,
                account_id=account.id,
                stock_id=stock.id,
                trade_type=data['trade_type'],
                price=data['price'],
                shares=data['shares'],
            )
            session.add(trade)
        return self.success_response('ok')

    @validate_request_json
    def post(self, id):
        """
        Buy a stock with given `symbol`, `shares` and `price`.

        Params
        ------
        id : int
            Account identifier.
        """
        result = {}
        schema = TradeSchema()
        try:
            data = schema.loads(request.get_data())
        except ValidationError as err:
            return self.error_response(err.messages, self.HTTP_BAD_REQUEST)
        data['account_id'] = id
        trade_type = 'buy'
        
        with db.session_scope() as session:
            account = session.query(Account).filter_by(id=id).first()
            if not account:
                return self.error_response(errors.ACCOUNT_DNE, self.HTTP_NOT_FOUND)

            for stock in account.stocks:
                if stock.symbol == data['symbol']:
                    return self.error_response(errors.STOCK_EXISTS, self.HTTP_METHOD_NOT_ALLOWED)

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
                result['stock_id'] = s_id

                ar_schema = AccountReadSchema()
                ar_data = ar_schema.dump(account)
                result['account'] = ar_data

                trade = Trade(
                    user_id=account.user_id,
                    account_id=account.id,
                    stock_id=s_id,
                    trade_type=trade_type,
                    price=data['price'],
                    shares=data['shares'],
                )
                session.add(trade)
        return self.success_response(result=result, status_code=self.HTTP_CREATED)

accounts_ns.add_resource(AccountResource, '', methods=['POST', 'GET', 'DELETE'])
accounts_ns.add_resource(AccountResource, '/<string:action>', methods=['PATCH'])
accounts_ns.add_resource(StockResource, '/<int:id>/stocks', methods=['POST'])
accounts_ns.add_resource(StockResource, '/<int:id>/stocks/<int:stock_id>', methods=['PUT'])