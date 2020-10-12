from decimal import Decimal
from datetime import datetime
from marshmallow import validate, post_load, pre_dump
from marshmallow.fields import Float

from trader.extensions import ma

class UserVerifySchema(ma.Schema):
    email = ma.Str(required=True, validate=validate.Length(min=3, max=254))
    password = ma.Str(required=True, validate=validate.Length(min=8, max=30), load_only=True)

class UserSchema(UserVerifySchema):
    id = ma.Integer(dump_only=True)
    first_name = ma.Str(required=True)
    last_name = ma.Str(required=True)

class ClientSchema(ma.Schema):
    client_id = ma.Str(required=True, validate=validate.Length(equal=32))
    client_name = ma.Str(required=True, validate=validate.Length(equal=80))
    client_secret = ma.Str(required=True, validate=validate.Length(equal=64))
    redirect_uri = ma.Str(required=True, validate=validate.Length(max=2048))

class ScopeSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    scope = ma.Str(required=True, validate=validate.Length(min=1, max=100))

class ClientScopeSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    client_id = ma.Str(required=True, validate=validate.Length(equal=32))
    scope_id = ma.Integer(required=True)

class AccountReadSchema(ma.Schema):
    id = ma.Integer()
    user_id = ma.Integer()
    amt_change = ma.Decimal(places=2, as_string=True)
    pct_change = ma.Decimal(places=2, as_string=True)
    cash_amount = ma.Decimal(places=2, as_string=True)
    total_amount = ma.Decimal(places=2, as_string=True)
    equity_amount = ma.Decimal(places=2, as_string=True)
    initial_amount = ma.Decimal(places=2, as_string=True)
    last_name = ma.Str()

    @pre_dump
    def calculate_totals(self, data, many, **kwargs):
        """
        Calculate account total from the current cash and equity and account percent change 
        (gain or loss) since the initial amount at the time of account creation.
        """
        data.total_amount = data.cash_amount + data.equity_amount
        if data.total_amount < data.initial_amount:
            data.amt_change = data.total_amount - data.initial_amount
            data.pct_change = (-1)*round(abs(data.amt_change)/data.initial_amount, 2)*100
        elif data.initial_amount < data.total_amount:
            data.amt_change = data.total_amount - data.initial_amount
            data.pct_change = round(data.amt_change/data.initial_amount, 2)*100
        else:
            data.amt_change = 0
            data.pct_change = 0
        return data

    @pre_dump
    def calculate_pct_change(self, data, many, **kwargs):
        """
        Calculate 
        """
        data.pct_change = data.cash_amount + data.equity_amount
        return data

class AccountCreationSchema(ma.Schema):
    equity_amount = Float(default=float(0.00), validate=validate.Range(min=500))
    initial_amount = Float(required=True, validate=validate.Range(min=500))

    @post_load
    def set_cash_amount(self, data, **kwargs):
        data['cash_amount'] = data['initial_amount']
        return data

class AccountUpdateSchema(ma.Schema):
    amount = Float(required=True, validate=validate.Range(min=20))

class TradeSchema(ma.Schema):
    account_id = ma.Integer(dump_only=True)
    price = Float(required=True, validate=validate.Range(min=0))
    process_date = ma.DateTime(missing=datetime.today())
    shares = ma.Integer(required=True, validate=validate.Range(min=1))
    symbol = ma.Str(required=True, validate=validate.Length(min=1, max=5))
    trade_type = ma.Str(load_only=True, validate=validate.OneOf(choices=['buy', 'sell']))
    
    @post_load
    def calculate_trade(self, data, **kwargs):
        """
        Determine total amount of a trade.
        """
        data['amount'] = round(float(data['shares']*data['price']), 2)
        return data