# encoding: utf-8
from db_sqlalchemy import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_pass = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    fav_stock_list = db.Column(db.String(255), nullable=True)
    my_stocks = db.Column(db.String(255), nullable=True)

    def __init__(self, uname, upass, email, favstocklist=None, mystocks=None):
        self.user_name = uname
        self.user_pass = upass
        self.email = email
        self.fav_stock_list = favstocklist
        self.my_stocks = mystocks

    def __repr__(self):
        return '<User: %r>' % self.uid
