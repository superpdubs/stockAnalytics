#encoding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


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
