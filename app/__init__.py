import os
import sys
import logging

from flask import Flask
from flask_restplus import Api, Resource, fields

from app.extensions import ma
from app.core.db import init_db
from app.resources import API_NAMESPACES

# Simple logging instantiation.
LOG_FILENAME = './logs/trading-simulator.log'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler(sys.stdout)
    ]
)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('app.cfg', silent=True)
    
    init_db(app)
    
    api = Api(app, version='1.0', title='Trading Simulator API',
        description='A simple API developed for the stock trading simulation application of the same name.',
    )
    ma.init_app(app)

    for ns in API_NAMESPACES:
        api.add_namespace(*ns)

    from app.core.db import redis

    @app.route("/test")
    def test():
        counter = redis.incr("counter")
        return "<b>Count:</b> {}".format(counter)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from app.core.db import Session
        Session.remove()

    return app