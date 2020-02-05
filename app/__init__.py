import os
import sys
import logging
import traceback

from flask import Flask
from werkzeug.exceptions import HTTPException
from flask_restplus import Api, Resource, fields

from app.lib import errors
from app.extensions import ma
from app.database import init_db
from app.resources import API_NAMESPACES

# Simple logging setup
file_handler = logging.handlers.RotatingFileHandler('./logs/trading-simulator.log', maxBytes=10000)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        file_handler,
        logging.StreamHandler(sys.stdout)
    ]
)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    init_db(app)
    
    api = Api(app, version='1.0', title='Trading Simulator API',
        description='A simple API developed for the stock trading simulation application of the same name.',
    )
    ma.init_app(app)

    for ns in API_NAMESPACES:
        api.add_namespace(*ns)

    from app.database import redis

    @app.route("/test")
    def test():
        counter = redis.incr("counter")
        return "<b>Count:</b> {}".format(counter)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from app.database import Session
        Session.remove()

    @app.errorhandler(Exception)
    def handle_exception(e):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logging.error(str(e))
        logging.error('\n' + ''.join(traceback.format_tb(exc_traceback)))

        if isinstance(e, HTTPException):
            response = { 'error': e.description }
            return response, e.code
        
        response = { 'error': errors.DEFAULT }
        return response, 500

    return app