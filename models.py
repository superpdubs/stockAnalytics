# encoding: utf-8
from db_sqlalchemy import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50),nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    fav_stock_list = db.Column(db.String(255), nullable=True)
    my_stocks = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '{} - {} - {}'.format(self.uid, self.firstname, self.lastname)

    def getName(self):
        return self.firstname

    def getId(self):
        return self.uid


class Stock(db.Model):

	__tablename__ = 'stock'

	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(10), unique=True, nullable = False)
	name=db.Column(db.String(50),unique=True,nullable=False)

	def __repr__(self):

		return '{} - {} - {}'.format(self.id, self.symbol, self.name)

	def as_dict(self):
		return {'symbol': self.symbol, 'name':self.name}

class PendingUser(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    code = db.Column(db.String(50), nullable=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50),nullable=False)
    user_pass = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '{} - {}'.format(self.email, self.code)
