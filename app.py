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
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

with app.app_context():
    db.create_all()


@app.route('/',methods=['GET','POST'])
def index():
    message = None
    if request.method == 'GET':
        message = request.args.get('message')
    stockform = StockForm()
    if stockform.validate_on_submit():
        this_stock = stockform.stock.data
        # Bypass loading page because this should only be used when
        # JavaScript is disabled / broken
        return redirect(url_for('stock', stockname=this_stock))
    uname = uname_getter()
    if uname != None:
        return render_template('index_loggedin.html', thisform=stockform, this_uname=uname, msg=message)
    return render_template('index_loggedout.html', thisform=stockform, this_uname=uname)


@app.route('/login', methods=['GET','POST'])
def login():
    if uname_getter() != None:
        return redirect(url_for('index'))
    loginform = LoginForm()
    loginvalidator = LoginValidator()
    msg = None
    if loginform.validate_on_submit():
        this_email = loginform.user_email.data
        this_password = loginform.user_pass.data
        this_login = {'email': this_email, 'password': this_password}
        msg = loginvalidator.validate(this_login)
        if msg is None:
            thisuser = User.query.filter(User.email == this_email).first()
            thisuid = thisuser.getId()
            session['uid'] = str(thisuid)
            return redirect(url_for('index'))
    return render_template('login.html',thisform=loginform, info=msg, this_uname=uname_getter())


@app.route('/logout')
def logout():
    session['uid'] = None
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if uname_getter() != None:
        return redirect(url_for('index'))
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
            verification = Verfication()
            mail = VerificationEmail()
            verifyCode = verification.generate_code()
            if mail.sendto(this_email,verifyCode) is not None:
                err_msg = 'Verification email failed to send, try again'
            else:
                pending_user = PendingUser(email=this_email,
                                           code=verifyCode,
                                           firstname=this_firstname,
                                           lastname=this_lastname,
                                           user_pass=this_pass)
                db.session.add(pending_user)
                db.session.commit()
                return render_template("checkemail.html")

        msg = err_msg

    return render_template('register.html',thisform=registerform,info=msg, this_uname=uname_getter())


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
                           company=company,
                           this_uname=uname_getter())


@app.route('/check_email' , methods=['GET'])
def check_email():
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


@app.route('/verify_email' , methods=['GET'])
def verify_email():
    if request.method != 'GET':
        return redirect(url_for('index'))
    email = request.args.get('email')
    code = request.args.get('code')
    user = PendingUser.query.filter(PendingUser.email == email).first()
    if user is None:
        # TODO return page with expired link text
        return redirect(url_for('index'))
    if user.code == code:
        new_user = User(firstname=user.firstname,
                        lastname=user.lastname,
                        user_pass=user.user_pass,
                        email=user.email,
                        fav_stock_list=None,
                        my_stocks=None)
        db.session.add(new_user)
        db.session.delete(user)
        db.session.commit()
        session['uid'] = str(new_user.getId())
        return redirect(url_for('index', message='Account successfully created'))


@app.route('/stocks')
def suggestions():
    query = request.args.get('q').upper()
    res = Stock.query.all()
    list_stocks = [r.as_dict() for r in res]
    result = []
    for e in list_stocks:
        if (e.get('name').upper().find(query) == 0):
            result.append(e)
            # limit results to 10 max
            if (len(result) == 10):
                break
    return jsonify(result)

@app.route('/sources')
def sources():
    stockForm = StockForm()
    return render_template('sources.html', thisform=stockForm, this_uname=uname_getter())


@app.context_processor
def utility_processor():
    def twitterEmbed(statusId, url):
        return search.twitterEmbed(status_id=statusId, url=url)

    return dict(twitterEmbed=twitterEmbed)

def uname_getter():
    thisuser = User.query.filter(User.uid == session.get('uid')).first()
    if thisuser is None:
        return None
    else:
        return thisuser.getName()

if __name__ == '__main__':
    app.run(debug=True)
