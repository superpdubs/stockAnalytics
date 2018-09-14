#encoding: utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo,InputRequired


class StickerForm(FlaskForm):
    sticker = StringField('Sticker', validators=[DataRequired(message='Stock name could not be empty')], render_kw={"placeholder": "Stock Name"})
    submit = SubmitField('Go Fetch !')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')
