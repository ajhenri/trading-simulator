import os
import sys
import logging
import logging.handlers
import datetime
import traceback

from flask import Flask, Blueprint, request, redirect, render_template
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect
from flask_restplus import Api, Resource, fields

from trader.lib import errors
from trader.models import User
from trader.extensions import ma, db
from trader.views.auth import auth_bp
from trader.resources import API_NAMESPACES

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
    app = Flask(__name__, instance_relative_config=True, template_folder='templates', 
        static_folder='frontend')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    csrf = CSRFProtect(app)

    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api = Api(api_bp, version='1.0', title='Trading Simulator API',
        description='A simple API developed for the stock trading simulation application of the same name.',
    )
    csrf.exempt(api_bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    ma.init_app(app)

    for ns in API_NAMESPACES:
        api.add_namespace(*ns)

    @login_manager.user_loader
    def load_user(user_id):
        with db.session_scope() as session:
            return session.query(User).filter_by(id=user_id).first()
        return False

    @app.route("/test")
    def test():
        counter = db.redis.incr("counter")
        return "<b>Count:</b> {}".format(counter)

    @app.route('/')
    @app.route('/account', endpoint='account')
    @app.route('/trade', endpoint='trade')
    @app.route('/activity', endpoint='activty')
    @login_required
    def index():
        return render_template('index.html')

    @app.context_processor
    def inject_date():
        return { 'now': datetime.datetime.utcnow() }

    #TODO: Error handling across API and Application.
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     exc_type, exc_value, exc_traceback = sys.exc_info()
    #     logging.error(str(e))
    #     logging.error('\n' + ''.join(traceback.format_tb(exc_traceback)))

    #     if request.path.startswith('/api/'):
    #         if isinstance(e, HTTPException):
    #             response = { 'error': e.description }
    #             return response, e.code
            
    #         response = { 'error': errors.DEFAULT }
    #         return response, 500
    #     else:
    #         if hasattr(e, 'code') and e.code == 404:
    #             return render_template('errors/404.html')
    #         else:
    #             return render_template('errors/500.html')

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    return app