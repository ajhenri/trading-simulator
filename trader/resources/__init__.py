from .users import users_ns
from .accounts import accounts_ns
from .exchange import exchange_ns

API_NAMESPACES = [
    (users_ns, '/users'),
    (accounts_ns, '/accounts'),
    (exchange_ns, '/exchange')
]