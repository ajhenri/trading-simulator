import bcrypt

from flask import Flask, Blueprint, request, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from trader.models import User
from trader.extensions import db
from trader.lib.definitions import ResponseErrors
from trader.schemas.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

def authenticate_user(email, password):
    with db.session_scope() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            return False

        password = bcrypt.hashpw(password.encode(), user.salt)
        if password == user.password:
            login_user(user)
            return user
        return False

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        with db.session_scope() as session:
            user = authenticate_user(form.email.data, form.password.data)
            if not user:
                return render_template('login.html', form=form, error=ResponseErrors.INVALID_LOGIN)
            
            if current_user.is_authenticated:
                return redirect(url_for('account'))
            return render_template('login.html', form=form, error=ResponseErrors.INVALID_LOGIN)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        with db.session_scope() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
            if user:
                return render_template('register.html', form=form, 
                    error='User with this email address already exists')

            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(form.password.data.encode(), salt)

            user_input = {
                'email': form.email.data,
                'password': hashed_pw,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'salt': salt
            }
            user = User(**user_input)
            session.add(user)
            session.flush()

            login_user(user, force=True)

            if current_user.is_authenticated:
                return redirect(url_for('account'))
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout/', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))