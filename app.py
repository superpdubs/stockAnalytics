#encoding: utf-8
from flask import Flask, redirect, url_for, render_template, request, jsonify,session
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
app.config.update(SECRET_KEY='a secret kry')
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

    return render_template('index.html', thisform=stockform, this_uname= None)


@app.route('/login_uid/<login_uid>',methods=['GET','POST'])
def index_withId(login_uid):
    stockform = StockForm()
    if stockform.validate_on_submit():
        this_stock = stockform.stock.data
        # Bypass loading page because this should only be used when
        # JavaScript is disabled / broken
        return redirect(url_for('stock', stockname=this_stock))
    thisuser = User.query.filter(User.uid == login_uid).first()
    thisuname = thisuser.getName()
    return render_template('index.html', thisform=stockform, this_uname= thisuname,this_uid = login_uid)


@app.route('/login', methods=['GET','POST'])
def login():
    loginform = LoginForm()
    loginvalidator = LoginValidator()
    msg =""
    if loginform.validate_on_submit():
        this_email = loginform.user_email.data
        this_password = loginform.user_pass.data
        this_login = {'email': this_email, 'password': this_password}
        msg = loginvalidator.validate(this_login)
        if msg is None:
            thisuser = User.query.filter(User.email == this_email).first()
            thisuid = thisuser.getId()
            # set this uid = true, which means user status : login
            session[str(thisuid)] = True
            return redirect(url_for('index_withId',login_uid=str(thisuid)))
    return render_template('login.html',thisform=loginform, info=msg)


@app.route('/logout/<this_uid>')
def logout(this_uid):
    session[this_uid] = False
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    registerform = RegistrationForm()
    registervalidator = RegisterValidator()
    msg = None
    if registerform.validate_on_submit():
        this_firstname = registerform.firstname.data
        this_lastname = registerform.lastname.data
        this_email = registerform.email.data
        this_pass = registerform.user_pass.data
        this_cpass = registerform.confirm.data
        this_vcode = registerform.verification.data
        this_registration = {'firstname':this_firstname,'lastname': this_lastname, 'password': this_pass,
                     'email': this_email,'cpass':this_cpass,'vcode':this_vcode}
        err_msg = registervalidator.validate(this_registration);
        if err_msg is None:
            valid_user = User(this_firstname,this_lastname,this_pass, this_email)
            db.session.add(valid_user)
            db.session.commit()
            return render_template("reg_success.html", login_id=this_email)
        else:
            msg = err_msg

    return render_template('register.html',thisform=registerform,info=msg)


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


@app.route('/verify_email' , methods=['GET'])
def verify_email():
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
    verification = Verfication()
    mail = VerificationEmail()
    send = False
    if request.method == 'GET':
        thisemail = request.args.get('this_email')
        verifyCode = verification.generate_code()
        # store (user-email,verifycode) in session
        session[thisemail] = verifyCode
        if len(verifyCode) == 6:
            mail.sendto(thisemail,verifyCode)
            send = True
        else:
            send = False

    return jsonify(send=send)


@app.route('/stocks')
def suggestions():
    query = request.args.get('q').upper()
    res = Stock.query.all()
    list_stocks = [r.as_dict() for r in res]
    result = []
    for e in list_stocks:
        if (e.get('symbol').find(query) == 0):
            result.append(e)
            # limit results to 10 max
            if (len(result) == 10):
                break
    return jsonify(result)

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
