# encoding: utf-8
from db_sqlalchemy import db
from sqlalchemy import Column, Integer, String

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
		return '<User_id: %r  | User_name: %s>' % (self.uid , self.user_name)

class Stock(db.Model):
	__tablename__ = 'stock'

	id = db.Column(db.Integer, primary_key=True)
	symbol = db.Column(db.String(10), unique=True, nullable = False)
	name=db.Column(db.String(50),unique=True,nullable=False)

	def __repr__(self):

		return '{} - {} - {}'.format(self.id, self.symbol, self.name)

	def as_dict(self):
		return {'symbol': self.symbol, 'name':self.name}
