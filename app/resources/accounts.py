import logging
import decimal

from flask import request
from marshmallow import ValidationError
from flask_restplus import Namespace, Resource, fields

from app.database import session_scope
from app.schemas import AccountSchema, AccountCreationSchema, \
    AccountPositionSchema
from app.models import Account, Position, TradeLogEntry
from app.utils.trades import calculate_trade
from app.resources.base_resource import BaseResource
from app.services.third_party.wtd import WorldTradingData

accounts_ns = Namespace('accounts', description='Account API Functions')

@accounts_ns.doc()
class AccountResource(BaseResource):
    def get(self, id):
        """
        Get account information such as cash and equity totals, as well as
        list of currently held positions.

        Params
        ------
        id : int
            Account identifier.
        """
        try:
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response('Account does not exist', 404)

                positions = {}
                for position in account.positions:
                    positions[position.ticker] = {
                        'id': position.id, 
                        'ticker': position.ticker, 
                        'shares': position.number_of_shares,
                        'bought_at': position.bought_at
                    }

                stock_list = positions.keys()
                if len(stock_list) > 0:
                    stocks = WorldTradingData().get_stocks(stock_list)
                    stocks = stocks['data']
                    for stock in stocks:
                        if stock['symbol'] in positions:
                            positions[stock['symbol']]['price'] = float(stock['price'])

                schema = AccountSchema()
                data = schema.dump(account)
                data['positions'] = positions
        except Exception as e:
            logging.error(str(e))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)            

        return self.success_response(data)

    def patch(self, id):
        """
        Update the amount of available "cash" in the specified account.

        Params
        ------
        id : int
            Account identifier.
        """
        try:
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response('Account does not exist', 404)

                data = request.get_json()
                if not data['cash_amount']:
                    return self.error_response({"cash_amount": ["Missing data for required field."]}, 400)
                
                data['cash_amount'] = decimal.Decimal(data['cash_amount'])
                account.cash_amount = data['cash_amount']
        except Exception as e:
            logging.error(str(e))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)
        
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
                    return self.error_response('Account already exists for this user')
                
                account = Account(**data)
                session.add(account)
                session.flush()

                created_account_id = account.id
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)

        if not created_account_id:
            return self.error_response('Account was not created')
        return self.success_response(result={'id': created_account_id}, status_code=201)

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
                    return self.error_response('Account does not exist', 400)
                account.delete()
        except Exception as err:
            logging.error(str(err))
            return self.error_response('Error deleting account')
        return self.success_response(result='ok')

@accounts_ns.doc()
class AccountPositionResource(BaseResource):
    def put(self, id, position_id):
        """
        Trade (buy or sell) more of the specified position.

        Params
        ------
        id : int
            Account identifier.
        position_id : int
            Account position identifier.
        """
        result = {}
        try:
            schema = AccountPositionSchema()
            data = schema.loads(request.get_data())
            cost = calculate_trade(data['number_of_shares'], data['bought_at'], Account.BROKERAGE_FEE)

            with session_scope() as session:
                account = session.query(Account).\
                    join(Account.positions).\
                    filter(Account.id == id, Position.id == position_id).first()

                if not account:
                    return self.error_response('Position does not exist', 404)

                position = account.positions[0]
                if data['trade'] == 'buy':
                    if account.cash_amount < cost:
                        return self.success_response(result='Not enough funds to buy this many shares', success=False)
                    position.number_of_shares += data['number_of_shares']
                    account.cash_amount -= cost
                    account.equity_amount += cost
                elif data['trade'] == 'sell':
                    if position.number_of_shares < data['number_of_shares']:
                        return self.error_response('Shares passed is greater than what is owned', 400)
                    position.number_of_shares -= data['number_of_shares']
                    account.cash_amount += cost
                    account.equity_amount -= cost
                else:
                    return self.error_response('Incorrect trade type', 400)

                log = TradeLogEntry(
                    user_id=account.user_id,
                    account_id=account.id,
                    position_id=position.id,
                    trade_type=data['trade'],
                    ticker=data['ticker'],
                    price=data['bought_at'],
                    number_of_shares=data['number_of_shares'],
                )
                session.add(log)
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)
        return self.success_response('ok')

    def post(self, id):
        """
        Buy a position, based on given `ticker`, `number_of_shares` and `bought_at` price.

        Params
        ------
        id : int
            Account identifier.
        """
        result = {}
        try:
            schema = AccountPositionSchema()
            data = schema.loads(request.get_data())
            data['account_id'] = id

            data['cost'] = calculate_trade(data['number_of_shares'], data['bought_at'], Account.BROKERAGE_FEE)
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response('Account does not exist', 404)
                if account.cash_amount < data['cost']:
                    return self.success_response(result='Not enough funds to buy this position', success=False)

                existing_p = session.query(Position).filter_by(account_id=id, ticker=data['ticker']).first()
                if existing_p:
                    return self.success_response(result='Position already exists', success=False)

                p = Position(**data)
                session.add(p)
                session.flush()

                p_id = p.id
                if p_id:
                    account.cash_amount -= data['cost']
                    account.equity_amount += data['cost']
                    result['id'] = p_id
                    result['account'] = {'cash': account.cash_amount, 'equity': account.equity_amount}

                log = TradeLogEntry(
                    user_id=account.user_id,
                    account_id=account.id,
                    position_id=p_id,
                    trade_type='buy',
                    ticker=data['ticker'],
                    price=data['bought_at'],
                    number_of_shares=data['number_of_shares'],
                )
                session.add(log)
        except ValidationError as err:
            logging.debug(err)
            return self.error_response(err.messages)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)

        if not p_id:
            return self.error_response('Account position was not created')
        return self.success_response(result=result, status_code=201)
    
    def delete(self, id, position_id):
        """
        Sell all of the specified position.

        Params
        ------
        id : int
            Account identifier.
        position_id : int
            Account position identifier.
        """
        try:
            with session_scope() as session:
                account = session.query(Account).filter_by(id=id).first()
                if not account:
                    return self.error_response('Account does not exist', 404)
                position = session.query(Position).filter_by(id=position_id, account_id=id).first()

                stocks = WorldTradingData().get_stocks([position.ticker])
                if len(stocks['data']['result']) != 1:
                    logging.debug(stocks['data']['result'])
                    return self.error_response(self.DEFAULT_ERROR_MESSAGE)
                
                data = stock['data']['result'][0]
                
                sale = round((position.number_of_shares*decimal.Decimal(data['price'])), 2)
                sale -= Account.BROKERAGE_FEE

                log = TradeLogEntry(
                    user_id=account.user_id,
                    account_id=account.id,
                    position_id=position_id,
                    trade_type='sell',
                    ticker=position.ticker,
                    price=data['price'],
                    number_of_shares=position.number_of_shares,
                )

                position.delete()
                account.cash_amount += sale

                session.add(log)
        except Exception as err:
            logging.error(str(err))
            return self.error_response(self.DEFAULT_ERROR_MESSAGE)
        return self.success_response(result='ok')

accounts_ns.add_resource(AccountResource, '', methods=['POST'])
accounts_ns.add_resource(AccountResource, '/<id>', methods=['GET', 'PATCH', 'DELETE'])
accounts_ns.add_resource(AccountPositionResource, '/<id>/positions', methods=['POST'])
accounts_ns.add_resource(AccountPositionResource, '/<id>/positions/<position_id>', methods=['PUT', 'DELETE'])