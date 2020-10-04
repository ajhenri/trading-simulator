import logging
from decimal import Decimal
from datetime import datetime
from http import HTTPStatus

from flask import request, Blueprint
from marshmallow import ValidationError
from flask_login import login_required, current_user
from flask_restful import Api, Resource

from trader.lib.definitions import ResponseErrors
from trader.extensions import db
from trader.schemas import AccountReadSchema, AccountCreationSchema, \
    AccountUpdateSchema, TradeSchema
from trader.models import Account, Stock, Trade
from trader.resources.base_resource import BaseResource, validate_request_json

accounts_bp = Blueprint('accounts', __name__)
accounts = Api(accounts_bp)

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
                return self.error_response(ResponseErrors.ACCOUNT_DNE, HTTPStatus.NOT_FOUND)

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
                stock_data = self.iex_api.get_stock_data(stock_list)
                for symb, stock in stock_data.items():
                    if symb in stocks:
                        stocks[symb]['price'] = "{0:.2f}".format(float(stock['quote']['latestPrice']))

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
            return self.error_response(ResponseErrors.ACCOUNT_INVALID_ACTION, HTTPStatus.BAD_REQUEST)

        with db.session_scope() as session:
            account = session.query(Account).filter_by(user_id=current_user.id).first()
            if not account:
                return self.error_response(ResponseErrors.ACCOUNT_DNE, HTTPStatus.NOT_FOUND)

            schema = AccountUpdateSchema()
            try:
                data = schema.loads(request.get_data())
            except ValidationError as err:
                return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)
            
            if action == 'deposit':
                account.cash_amount += data['amount']
            elif action == 'withdraw' and account.cash_amount >= data['amount']:
                account.cash_amount -= data['amount']
            else:
                return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)
        
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
            return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)
        
        with db.session_scope() as session:
            account = session.query(Account).filter_by(user_id=current_user.id).first()
            if account:
                return self.error_response(ResponseErrors.ACCOUNT_EXISTS, HTTPStatus.BAD_REQUEST)
            
            data['user_id'] = current_user.id

            account = Account(**data)
            session.add(account)
            session.flush()

            created_account_id = account.id

        return self.success_response(result={'id': created_account_id}, status_code=HTTPStatus.CREATED)

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
            account = session.query(Account).filter_by(user_id=current_user.id)
            if not account:
                return self.error_response(ResponseErrors.ACCOUNT_DNE, HTTPStatus.NOT_FOUND)
            account.delete()
        return self.success_response(result='ok')

class StockResource(BaseResource):

    @login_required
    @validate_request_json
    def put(self, account_id, stock_id):
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
            return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)
        
        with db.session_scope() as session:
            account = session.query(Account).\
                join(Account.stocks).\
                filter(Account.id == account_id, Stock.id == stock_id, Stock.symbol == data['symbol']).first()

            if not account:
                return self.error_response(ResponseErrors.STOCK_DNE, HTTPStatus.NOT_FOUND)
            if account.user_id != current_user.id:
                return self.error_response(ResponseErrors.ACCOUNT_NO_ACCESS, HTTPStatus.FORBIDDEN)
            
            delete_flag = False
            stock = account.stocks[0]
            if data['trade_type'] == 'buy':
                cost = data['amount'] + Account.BROKERAGE_FEE
                if account.cash_amount < cost:
                    return self.success_response(result=ResponseErrors.NOT_ENOUGH_FUNDS, success=False)
                stock.shares += data['shares']
                account.cash_amount -= cost
                account.equity_amount += data['amount']
            elif data['trade_type'] == 'sell':
                if account.cash_amount < Account.BROKERAGE_FEE:
                    return self.success_response(result=ResponseErrors.NOT_ENOUGH_FUNDS, success=False)
                if stock.shares < data['shares']:
                    return self.success_response(result=ResponseErrors.TOO_MANY_SHARES, success=False)
                if stock.shares == data['shares']:
                    delete_flag = True
                    stock.sold_on = data['process_date']
                stock.shares -= data['shares']
                account.cash_amount -= Account.BROKERAGE_FEE
                account.cash_amount += data['amount']
                account.equity_amount -= (stock.bought_at*data['shares'])

            trade = Trade(
                user_id=account.user_id,
                account_id=account.id,
                stock_id=stock.id,
                trade_type=data['trade_type'],
                price=data['price'],
                shares=data['shares'],
            )
            session.add(trade)

            if delete_flag:
                session.query(Stock).filter(Stock.id==stock_id).delete()

        return self.success_response('ok')

    @login_required
    @validate_request_json
    def post(self, account_id):
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
            return self.error_response(err.messages, HTTPStatus.BAD_REQUEST)
        data['account_id'] = account_id
        trade_type = 'buy'
        
        with db.session_scope() as session:
            account = session.query(Account).filter_by(id=account_id).first()
            if not account:
                return self.error_response(ResponseErrors.ACCOUNT_DNE, HTTPStatus.NOT_FOUND)
            if account.user_id != current_user.id:
                return self.error_response(ResponseErrors.ACCOUNT_NO_ACCESS, HTTPStatus.FORBIDDEN)

            for stock in account.stocks:
                if stock.symbol == data['symbol']:
                    return self.error_response(ResponseErrors.STOCK_EXISTS, HTTPStatus.METHOD_NOT_ALLOWED)

            total = data['amount'] + Account.BROKERAGE_FEE
            if account.cash_amount < total:
                return self.success_response(result=ResponseErrors.NOT_ENOUGH_FUNDS, success=False)

            existing_s = session.query(Stock).filter_by(account_id=account_id, symbol=data['symbol']).first()
            if existing_s:
                return self.error_response(ResponseErrors.STOCK_EXISTS, HTTPStatus.BAD_REQUEST)

            s = Stock(
                account_id=account_id,
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
        return self.success_response(result=result, status_code=HTTPStatus.CREATED)

accounts.add_resource(AccountResource, '', methods=['POST', 'GET', 'DELETE'])
accounts.add_resource(AccountResource, '/<string:action>', methods=['PATCH'], endpoint='account_patch')
accounts.add_resource(StockResource, '/<int:account_id>/stocks', methods=['POST'])
accounts.add_resource(StockResource, '/<int:account_id>/stocks/<int:stock_id>', methods=['PUT'], endpoint='stock_update')