from decimal import Decimal
from datetime import datetime
from marshmallow import validate, post_load

from app.extensions import ma

class UserVerifySchema(ma.Schema):
    username = ma.Str(required=True, validate=validate.Length(min=2, max=80))
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

class AccountSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    user_id = ma.Integer(required=True, load_only=True)
    cash_amount = ma.Str(required=True)
    equity_amount = ma.Str(required=True)
    initial_amount = ma.Str(required=True)
    last_name = ma.Str(required=True)

class AccountCreationSchema(ma.Schema):
    user_id = ma.Integer(required=True)
    equity_amount = ma.Decimal(default=Decimal(0.00))
    initial_amount = ma.Decimal(required=True)

    @post_load
    def set_cash_amount(self, data, **kwargs):
        data['cash_amount'] = data['initial_amount']
        return data

class AccountUpdateSchema(ma.Schema):
    amount = ma.Decimal(required=True)

class TradeSchema(ma.Schema):
    account_id = ma.Integer(dump_only=True)
    price = ma.Decimal(required=True)
    process_date = ma.DateTime(missing=datetime.today())
    shares = ma.Integer(required=True, validate=validate.Range(min=1))
    symbol = ma.Str(required=True, validate=validate.Length(min=1, max=5))
    trade_type = ma.Str(load_only=True, validate=validate.OneOf(choices=['buy', 'sell']))
    
    @post_load
    def calculate_trade(self, data, **kwargs):
        """
        Determine total amount of a trade.
        """
        data['amount'] = round(Decimal(shares*price), 2)
        return data