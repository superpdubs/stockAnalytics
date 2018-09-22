# encoding: utf-8
from db_sqlalchemy import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50),nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    fav_stock_list = db.Column(db.String(255), nullable=True)
    my_stocks = db.Column(db.String(255), nullable=True)



    def __init__(self,fname,lname,upass,email,favstocklist=None,mystocks=None):
        self.firstname = fname
        self.lastname = lname
        self.user_pass = upass
        self.email = email
        self.fav_stock_list = favstocklist
        self.my_stocks = mystocks

    def __repr__(self):
        return '<User_id: %r  | User_name: %s>' % (self.uid , self.firstname)
