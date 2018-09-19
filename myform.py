#encoding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo,InputRequired


class StockForm(FlaskForm):
    stock = StringField('Stock', render_kw={"placeholder": "Stock Name"})
    submit = SubmitField('Go Fetch !')


class RegistrationForm(FlaskForm):
    username = StringField('Username')
    email = StringField('Email Address')
    password = PasswordField('New Password')
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
