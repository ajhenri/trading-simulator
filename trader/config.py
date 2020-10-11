from os import environ, path
from instance import config as Config

class BaseConfig:
    """Base configuration to be extended."""
    ENV = environ.get('FLASK_ENV')
    SECRET_KEY = Config.SECRET_KEY
    STATIC_FOLDER = 'frontend'
    TEMPLATES_FOLDER = 'templates'
    WEBPACK_DEV_SERVER = 'http://localhost:9000'

class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    DATABASE_DRIVER = 'postgresql'
    DATABASE_HOST = Config.DATABASE_HOST
    DATABASE_NAME = Config.DATABASE_NAME
    DATABASE_USER = Config.DATABASE_USER
    DATABASE_PASS = Config.DATABASE_PASS
    IEX_API_URL = 'https://cloud.iexapis.com/stable'
    IEX_SECRET_TOKEN = Config.IEX_SECRET_TOKEN

class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    DATABASE_DRIVER = 'postgresql'
    DATABASE_HOST = Config.DATABASE_HOST
    DATABASE_NAME = Config.DATABASE_NAME
    DATABASE_USER = Config.DATABASE_USER
    DATABASE_PASS = Config.DATABASE_PASS
    IEX_API_URL = 'https://sandbox.iexapis.com/stable'
    IEX_SECRET_TOKEN = Config.IEX_SB_SECRET_TOKEN