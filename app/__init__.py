import os

from flask import Flask
from flask_restplus import Api, Resource, fields

from app.core.db import DBConnection
from app.resources import API_NAMESPACES

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('app.cfg', silent=True)
    
    DBConnection.init_app(app)
    
    api = Api(app, version='1.0', title='Trading Simulator API',
        description='A simple API developed for the stock trading simulation application of the same name.',
    )

    for ns in API_NAMESPACES:
        api.add_namespace(*ns)

    from app.core.db import redis

    @app.route("/test")
    def test():
        counter = redis.incr("counter")
        return "<b>Count:</b> {}".format(counter)

    return app