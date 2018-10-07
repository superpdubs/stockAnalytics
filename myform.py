#encoding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class StockForm(FlaskForm):
    stock = StringField('Stock', render_kw={"placeholder": "Search", "autocomplete": "off"})
    submit = SubmitField('Go Fetch !')


class EmailForm(FlaskForm):
    email = StringField('Email Address')
    verification = StringField('Verification Code')
    submit = SubmitField('Register')

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname')
    lastname = StringField('Lastname')
    email = StringField('Email Address')
    user_pass = PasswordField('Password')
    confirm = PasswordField('Confirm Password')
    verification = StringField('Verification Code')
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_email = StringField('Email')
    user_pass = PasswordField('Password')
    submit = SubmitField('Login')
