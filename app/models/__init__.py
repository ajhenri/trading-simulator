from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Binary, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr

Base = declarative_base()

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

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(Binary(60), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    client = relationship("OauthClient", uselist=False, back_populates="user")

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
    user = relationship("User", back_populates="client")
    scopes = relationship("OauthClientScope")

class OauthClientScope(Base):
    __tablename__ = 'oauth_client_scopes'
    id = Column(Integer, primary_key=True)
    client_id = Column(String(32), ForeignKey('oauth_clients.client_id'))
    scope_id = Column(Integer, ForeignKey('oauth_scopes.id'))
    scope = relationship("OauthScope")

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