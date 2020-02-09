from decimal import Decimal
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Enum, Integer, String, Binary, DateTime, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(Binary(60), nullable=False)
    salt = Column(Binary(40), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    client = relationship('OauthClient', uselist=False, back_populates='user')
    account = relationship('Account', uselist=False, backref='users')

class OauthGrantMixin(object):
    @declared_attr
    def user_id(cls):
        return Column(Integer, ForeignKey('users.id'))

    @declared_attr
    def client_id(cls):
        return Column(String(32), ForeignKey('oauth_clients.client_id'))
    
    @declared_attr
    def expires(cls):
        return Column(DateTime, default=datetime.utcnow)
    
    @declared_attr
    def scope(cls):
        return Column(String(100), nullable=False)

class OauthScope(Base):
    __tablename__ = 'oauth_scopes'
    id = Column(Integer, primary_key=True)
    scope = Column(String(100), nullable=False)

class OauthClient(Base):
    __tablename__ = 'oauth_clients'
    client_id = Column(String(32), primary_key=True)
    client_name = Column(String(80), nullable=False)
    client_secret = Column(String(64), nullable=False)
    redirect_uri = Column(String(2048), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='client')
    scopes = relationship('OauthClientScope')

class OauthClientScope(Base):
    __tablename__ = 'oauth_client_scopes'
    id = Column(Integer, primary_key=True)
    client_id = Column(String(32), ForeignKey('oauth_clients.client_id'))
    scope_id = Column(Integer, ForeignKey('oauth_scopes.id'))
    scope = relationship('OauthScope')

class OauthAccessToken(Base, OauthGrantMixin):
    __tablename__ = 'oauth_access_tokens'
    token = Column(String(40), primary_key=True)

class OauthRefreshToken(Base, OauthGrantMixin):
    __tablename__ = 'oauth_refresh_tokens'
    token = Column(String(40), primary_key=True)

class OauthAuthorizationCode(Base, OauthGrantMixin):
    __tablename__ = 'oauth_codes'
    code = Column(String(40), primary_key=True)
    redirect_uri = Column(String(2048), nullable=False)

class Account(Base):
    BROKERAGE_FEE = float('1.99')

    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cash_amount = Column(
        Numeric(precision=19, scale=2, asdecimal=False, decimal_return_scale=None), 
        default=0.00)
    equity_amount = Column(
        Numeric(precision=19, scale=2, asdecimal=False, decimal_return_scale=None), 
        default=0.00)
    initial_amount = Column(
        Numeric(precision=19, scale=2, asdecimal=False, decimal_return_scale=None), 
        default=0.00)
    stocks = relationship('Stock', cascade='all, delete-orphan')

class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id', onupdate='CASCADE', ondelete='CASCADE'))
    bought_at = Column(
        Numeric(precision=19, scale=2, asdecimal=False, decimal_return_scale=None), 
        nullable=False)
    bought_on = Column(DateTime, nullable=False)
    sold_on = Column(DateTime, default=None)
    initial_cost = Column(
        Numeric(precision=19, scale=2, asdecimal=False, decimal_return_scale=None), 
        nullable=False)
    shares = Column(Integer, nullable=False)
    symbol = Column(String(5), unique=True, nullable=False)

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    account_id = Column(Integer, nullable=False)
    stock_id = Column(Integer, nullable=False)
    trade_type = Column(Enum('buy', 'sell', native_enum=False), nullable=False)
    process_date = Column(DateTime, nullable=False, default=datetime.now)
    price = Column(
        Numeric(precision=19, scale=2, asdecimal=False, decimal_return_scale=None), 
        nullable=False)
    shares = Column(Integer, nullable=False)