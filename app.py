#encoding: utf-8
from flask import Flask, redirect, url_for, render_template
from models import *
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/feature')
def feature():
    return render_template('feature.html')


if __name__ == '__main__':
    app.run(debug=True)
