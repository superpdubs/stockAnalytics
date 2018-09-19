#encoding: utf-8
from flask import Flask, redirect, url_for, render_template, request
from models import *
import config
from myform import *
from resources import search
from validator import *
import time


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/line')
def line():

    price, date = search.pyEXChart("AAPL")
    line_labels=date[-7:]
    line_values=price[-7:]
    return render_template('line_chart.html', title='AAPL', max=500, labels=line_labels, values=line_values)


@app.route('/',methods=['GET','POST'])
def index():
    stockform = StockForm()
    # if method =='POST' and the user's input matches validator'srequirement
    # then return true
    # set csrf_token : OFF in config.py
    if stockform.validate_on_submit():
        this_stock = stockform.stock.data
        return redirect(url_for('stock', stockname=this_stock))

    return render_template('index.html', thisform=stockform)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    registerform = RegistrationForm()
    uservalidator = UserValidator()
    err_msg = None
    if registerform.validate_on_submit():
        this_username = registerform.username.data
        this_email = registerform.email.data
        this_password = registerform.password.data
        this_confirmpass = registerform.confirm.data
        this_user = {'name': this_username, 'password': this_password,
                     'email': this_email, 'confirmPass': this_confirmpass}
        err_msg = uservalidator.validate(this_user)
        if err_msg == None:
            # this_user = (this_username, this_password, this_email)
            # db.session.add(this_user)
            return ('register successfully')
        else:
            return render_template('register.html', thisform=registerform, error=err_msg)
    return render_template('register.html',thisform=registerform,error=err_msg)


@app.route('/stock/<stockname>')
def stock(stockname):
    # TODO: serverside validation of stock symbol
    tickerInfo = search.pyEXStockInfo(stockname)
    tickerNews = search.pyEXNews(stockname)
    # rand = plotStock(stockname)
    stockForm = StockForm()
    twitter = search.twitterAdvancedSearch(query="%24"+stockname, resultType="popular", count=20)
    delta = tickerInfo.get('currentPrice') - tickerInfo.get('open').get('price')
    percentage = delta / tickerInfo.get('open').get('price') * 100
    diff = 'loss'
    if delta > 0:
        delta = '+{:.2f}'.format(delta)
        diff = 'gain'
    else:
        delta = '{:.2f}'.format(delta)
    price, date = search.pyEXChart(stockname)
    line_labels=date
    line_values=price
    return render_template('stock.html',
                           thisform=stockForm,
                           tickerInfo=tickerInfo,
                           tickerNews=tickerNews,
                           twitter=twitter,
                           delta=delta,
                           percentage=percentage,
                           diff=diff,
                           labels=line_labels,
                           values=line_values,
                           max=tickerInfo['close']['price']*1.5)
                           # graph=rand)


@app.route('/feature')
def feature():
    return render_template('feature.html')


@app.route('/sources')
def sources():
    stockForm = StockForm()
    return render_template('sources.html', thisform=stockForm)


@app.context_processor
def utility_processor():
    def twitterEmbed(statusId, url):
        return search.twitterEmbed(status_id=statusId, url=url)

    return dict(twitterEmbed=twitterEmbed)


if __name__ == '__main__':
    app.run(debug=True)
