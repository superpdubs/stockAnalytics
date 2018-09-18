#encoding: utf-8
from flask import Flask, redirect, url_for, render_template, request
from models import *
import config
from myform import *
from stockPlot import plotStock
from resources import search
import time


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]


@app.route('/line')
def line():

    price, date = search.pyEXChart("AAPL")
    line_labels=date[-50:]
    line_values=price[-50:]
    return render_template('line_chart.html', title='AAPL', max=300, labels=line_labels, values=line_values)


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
    # TODO: serverside validation of stock symbol
    # cleanup graph images somehow
    tickerInfo = search.pyEXStockInfo(stockname)
    tickerNews = search.pyEXNews(stockname)
    # rand = plotStock(stockname)
    otherStickerForm = StickerForm()
    twitter = search.twitterAdvancedSearch(query=stockname, resultType="popular", count=20)
    delta = tickerInfo.get('currentPrice') - tickerInfo.get('open').get('price')
    percentage = delta / tickerInfo.get('open').get('price') * 100
    diff = 'loss'
    if delta > 0:
        delta = '+{:.2f}'.format(delta)
        diff = 'gain'
    return render_template('stock.html',
                           thisform=otherStickerForm,
                           tickerInfo=tickerInfo,
                           tickerNews=tickerNews,
                           twitter=twitter,
                           delta=delta,
                           percentage=percentage,
                           diff=diff)
                           # graph=rand)

@app.route('/feature')
def feature():
    return render_template('feature.html')

@app.route('/sources')
def sources():
    otherStickerForm = StickerForm()
    return render_template('sources.html', thisform=otherStickerForm)

@app.context_processor
def utility_processor():
    def twitterEmbed(statusId, url):
        return search.twitterEmbed(status_id=statusId, url=url)

    return dict(twitterEmbed=twitterEmbed)

if __name__ == '__main__':
    app.run(debug=True)
