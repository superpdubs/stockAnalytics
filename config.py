#encoding: utf-8

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///db/myfetch.db'

SQLALCHEMY_COMMIT_TEARDOWN = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = False
WTF_CSRF_SECRET_KEY = 'a random string'
