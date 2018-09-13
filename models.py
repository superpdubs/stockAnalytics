#encoding: utf-8
from db_sqlalchemy import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, uid, email):
        self.user_id = uid
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.user_id

