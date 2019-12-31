from app.extensions import ma
from marshmallow import validate

class UserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    username = ma.Str(required=True)
    password = ma.Str(required=True, load_only=True)
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