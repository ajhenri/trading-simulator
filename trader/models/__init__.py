from decimal import Decimal
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Enum, Integer, String, Binary, DateTime, Numeric, \
    UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(254), unique=True, nullable=False)
    password = Column(Binary(60), nullable=False)
    salt = Column(Binary(40), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    account = relationship('Account', uselist=False, backref='users')

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
    __table_args__ = (
        UniqueConstraint('account_id', 'symbol', name='stocks_akey'),
    )
    id = Column(Integer, primary_key=True)
    symbol = Column(String(5), nullable=False)
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