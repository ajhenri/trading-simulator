import decimal

from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, DecimalField
from wtforms.validators import Email, EqualTo, DataRequired, NumberRange, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), 
        EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])