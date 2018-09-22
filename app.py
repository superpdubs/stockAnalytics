#encoding: utf-8
from flask import Flask, redirect, url_for, render_template, request, jsonify
from models import *
import config
from myform import *
from resources import search
from validator import *
from codegenerator import *
from sendmail import *
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
    if stockform.validate_on_submit():
        this_stock = stockform.stock.data
        # Bypass loading page because this should only be used when
        # JavaScript is disabled / broken
        return redirect(url_for('stock', stockname=this_stock))
    return render_template('index.html', thisform=stockform)


@app.route('/fetching/<stockname>')
def fetching(stockname):
    return render_template('loading.html', stockname=stockname)


@app.route('/login', methods=['GET','POST'])
def login():
    loginform = LoginForm()
    loginvalidator = LoginValidator()
    msg =""
    if loginform.validate_on_submit():
        this_username = loginform.user_name.data
        this_password = loginform.user_pass.data
        this_login = {'name': this_username, 'password': this_password}
        msg = loginvalidator.validate(this_login)
    return render_template('login.html',thisform=loginform, info=msg)


@app.route('/register', methods=['GET','POST'])
def register():
    registerform = RegistrationForm()
    registervalidator = RegisterValidator()
    err_msg = None
    if registerform.validate_on_submit():
        this_firstname = registerform.firstname.data
        this_lastname = registerform.lastname.data
        this_email = registerform.email.data
        this_password = registerform.user_pass.data
        this_confirmpass = registerform.confirm.data
        # this_verify code = registerform.verification.data
        this_registration = {'firstname':this_firstname,'lastname': this_lastname, 'password': this_password,
                     'email': this_email, 'confirmPass': this_confirmpass}
        err_msg = registervalidator.validate(this_registration)
        if err_msg == None:
            valid_user = User('hi', this_password, this_email)
            db.session.add(valid_user)
            db.session.commit()
            err_msg = "Registration successfully! Try login!"

    return render_template('register.html',thisform=registerform,info=err_msg)


@app.route('/stock/<stockname>')
def stock(stockname):
    stockForm = StockForm()
    # TODO: serverside validation of stock symbol
    price, close, date, ohlc, company, news = search.iEXManualRequest(stockname.upper())

    twitter = search.twitterAdvancedSearch(query="%24"+stockname, resultType="popular", count=20)
    delta = price - ohlc["open"]["price"]
    percentage = delta / ohlc["open"]["price"] * 100
    diff = 'loss'
    if delta > 0:
        delta = '+{:.2f}'.format(delta)
        diff = 'gain'
    else:
        delta = '{:.2f}'.format(delta)
    return render_template('stock.html',
                           thisform=stockForm,
                           twitter=twitter,
                           delta=delta,
                           percentage=percentage,
                           diff=diff,
                           labels=date,
                           values=close,
                           price=price,
                           ohlc=ohlc,
                           news=news,
                           company=company
                           )


@app.route('/feature')
def feature():
    return render_template('feature.html')


@app.route('/email_verification')
def email_verify():
    emailform = EmailForm()
    return render_template('eval_email.html',thisform=emailform)


@app.route('/verify' , methods=['GET'])
def verify():
    msg =''
    emailvalidator = EmailValidator()
    if request.method == 'GET':
        eval_email = request.args.get('this_email')
        err_msg = emailvalidator.validate(eval_email)
        if err_msg is None :
            msg="This email could be used"
            eval = 1
        else:
            msg = err_msg
            eval = 0
    return jsonify(msg=msg,eval=eval)


@app.route('/sendcode' , methods=['GET'])
def send_vcode():
    send = 0
    msg = "Server is busy, please try again!"
    if request.method == 'GET':
        thisemail = request.args.get('this_email')
        verification = Verfication()
        verifyCode = verification.generate_code()
        mail = EmailVerification()
        if len(verifyCode) == 6:
            mail.sendto(thisemail,verifyCode)
            msg = 'Verification code already sent!'
            send = 1
        else:
            msg = "This should not happen!"
            send = 0

    return jsonify(msg=msg,send=send)



@app.route('/search')
def suggestions():
    query = request.args.get('q')
    # Return extra empty string in json so client knows it's an array
    return jsonify(query, '')

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
