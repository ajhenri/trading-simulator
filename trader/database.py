from contextlib import contextmanager
from redis import Redis, RedisError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

class TraderDB(object):
    """
    Simple object that handles database connectivity.
    """
    def __init__(self):
        self.engine = None
        self.Session = None

        # Stores
        self.redis = None

    def init_app(self, app):
        """
        Gather configuration data and create the SQLAlchemy engine and scoped
        session factory object to be used for calling the Session for database
        interaction. Redis is also initialized here, as an additional storage
        (or caching) option.
        """
        username = app.config['DATABASE_USER']
        password = app.config['DATABASE_PASS']
        driver = app.config['DATABASE_DRIVER']
        host = app.config['DATABASE_HOST']
        db = app.config['DATABASE_NAME']

        self.engine = create_engine('{}://{}:{}@{}/{}'.format(driver, username, password, host, db))
        self.Session = scoped_session(sessionmaker(bind=self.engine))

        self.redis = Redis(host='redis', db=0, socket_connect_timeout=2, socket_timeout=2)

        app.teardown_appcontext(self.teardown)

    def teardown(self, exception=None):
        self.Session.remove()

    @contextmanager
    def session_scope(self):
        """
        Taken from the SQLAlchemy documentation to be used as a context manager
        that simplifies committing database changes with the session object.
        As noted in the documentation, it "provides a transactional scope 
        around a series of operations."
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()