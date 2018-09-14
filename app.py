#encoding: utf-8
from flask import Flask, redirect, url_for, render_template, request
from models import *
import config
from myform import *

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/',methods=['GET','POST'])
def index():
    stickerform = StickerForm()
    # if method =='POST' and the user's input matches validator'srequirement
    # then return true
    # set csrf_token : OFF in config.py
    if stickerform.validate_on_submit():
        this_sticker = stickerform.sticker.data
        return redirect(url_for('stock',stockname=this_sticker))

    return render_template('index.html', thisform=stickerform)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    registerform = RegistrationForm()

    if registerform.validate_on_submit():
        this_username = registerform.username.data
        this_email = registerform.email.data
        this_password = registerform.password.data
        this_user = (this_username, this_password, this_email)
        print(this_user)
        # db.session.add(this_user)
        return ('register successfully')
    return render_template('register.html',thisform=registerform)


@app.route('/stock/<stockname>')
def stock(stockname):
    # Search any stock market info by this stock name
    # then show them in the following template
    # .....to implement.........
    otherStickerForm = StickerForm()
    return render_template('stock.html', stock_name=stockname, thisform=otherStickerForm)

@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/sources')
def sources():
    otherStickerForm = StickerForm()
    return render_template('sources.html', thisform=otherStickerForm)

if __name__ == '__main__':
    app.run(debug=True)
