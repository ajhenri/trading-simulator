import os
import sys
import base64
import logging
import logging.handlers
import datetime
import traceback

from flask import Flask, Blueprint, request, redirect, render_template, current_app
from werkzeug.exceptions import HTTPException
from flask_login import LoginManager, login_required
from flask_wtf.csrf import CSRFProtect

from trader.config import DevConfig, ProdConfig
from trader.models import User
from trader.extensions import ma, db
from trader.views.auth import auth_bp, authenticate_user
from trader.resources import api_blueprints
from trader.lib.definitions import ResponseErrors

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
    app = Flask(__name__, template_folder='templates', static_folder='frontend')

    env = os.environ.get('FLASK_ENV')
    if env == 'production':
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    db.init_app(app)

    csrf = CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    ma.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with db.session_scope() as session:
            return session.query(User).filter_by(id=user_id).first()
        return False

    @login_manager.request_loader
    def load_user_from_request(request):
        if request.method == "GET" and 'login' in request.path:
            return None
        
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_header = auth_header.replace('Basic ', '', 1)
        try:
            credentials = base64.b64decode(auth_header).decode()
            credentials = credentials.split(':')
            
            user = authenticate_user(credentials[0], credentials[1])
            return user
        except TypeError as e:
            logging.error({'exception': str(e)})
        
        return None

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
        return render_template('index.html', env=current_app.config['ENV'],
            dev_server=current_app.config['WEBPACK_DEV_SERVER'])

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
    
    with app.app_context():
        for bp in api_blueprints:
            csrf.exempt(bp[0])
            app.register_blueprint(bp[0], url_prefix='/api{}'.format(bp[1]))
        app.register_blueprint(auth_bp)

    return app