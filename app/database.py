from contextlib import contextmanager
from redis import Redis, RedisError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

redis = None
engine = None
Session = None

def init_db(app):
    """
    Initialize the DB and Redis storage mediums with constant values provided 
    by Flask's application object.
    A global "Redis" object, SQLAlchemy engine, and SQLAlchemy Session are created.
    
    Params
    ------
    app : The application object, an instance of `flask.Flask`.
    """
    global engine, Session, redis

    username = app.config['DATABASE_USER']
    password = app.config['DATABASE_PASS']
    driver = app.config['DATABASE_DRIVER']
    host = app.config['DATABASE_HOST']
    db = app.config['DATABASE_NAME']

    engine = create_engine('{}://{}:{}@{}/{}'.format(driver, username, password, host, db))
    Session = scoped_session(sessionmaker(bind=engine))

    redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)

@contextmanager
def session_scope():
    """
    Taken from the SQLAlchemy documentation to be used as a context manager
    that simplifies committing database changes with the session object.
    As noted in the documentation, it "provides a transactional scope 
    around a series of operations."
    """
    global Session
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()