from redis import Redis, RedisError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

redis = None
engine = None
session = None

class DBConnection:
    @classmethod
    def init_app(cls, app):
        global engine, session, redis

        username = app.config['DATABASE_USER']
        password = app.config['DATABASE_PASS']
        driver = app.config['DATABASE_DRIVER']
        host = app.config['DATABASE_HOST']
        db = app.config['DATABASE_NAME']

        engine = create_engine('{}://{}:{}@{}/{}'.format(driver, username, password, host, db))
        session = scoped_session(sessionmaker(bind=engine)())

        redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)

        from app import models
        
        models.Base.metadata.create_all(bind=engine)