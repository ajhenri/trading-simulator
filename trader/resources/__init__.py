from .users import users_bp
from .accounts import accounts_bp
from .exchange import exchange_bp

api_blueprints = [
    (users_bp, '/users'),
    (accounts_bp, '/accounts'),
    (exchange_bp, '/exchange')
]