#encoding: utf-8
from flask import Flask, redirect, url_for, render_template, request, jsonify,session
from models import *
import config
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


@app.route('/')
def index():
    if request.args.get('stock') != None:
        return redirect(url_for('stock', stockname=request.args.get('stock')))

    message = request.args.get('message')

    uname = uname_getter()
    if uname != None:
        return render_template('index_loggedin.html', this_uname=uname, msg=message)
    return render_template('index_loggedout.html', this_uname=uname)


@app.route('/login', methods=['GET','POST'])
def login():
    if uname_getter() != None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        this_email = request.form.get('user_email')
        this_password = request.form.get('user_pass')
        loginvalidator = LoginValidator()
        this_login = {'email': this_email, 'password': this_password}
        msg = loginvalidator.validate(this_login)
        if msg is None:
            thisuser = User.query.filter(User.email == this_email).first()
            thisuid = thisuser.getId()
            session['uid'] = str(thisuid)
            return redirect(url_for('index'))
        return render_template('login.html', info=msg, this_uname=None)
    return render_template('login.html', info=None, this_uname=None)


@app.route('/logout')
def logout():
    session['uid'] = None
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if uname_getter() != None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        this_firstname = request.form.get('firstname')
        this_lastname = request.form.get('lastname')
        this_email = request.form.get('email')
        this_pass = request.form.get('user_pass')
        this_cpass = request.form.get('confirm')
        registervalidator = RegisterValidator()
        this_registration = {'firstname':this_firstname,'lastname': this_lastname, 'password': this_pass,
                     'cpass':this_cpass,'email': this_email}
        msg = registervalidator.validate(this_registration);
        if msg is None:
            verification = Verfication()
            mail = VerificationEmail()
            verifyCode = verification.generate_code()
            if mail.sendto(this_email,verifyCode) is not None:
                msg = 'Registration failed, please try again later'
                return render_template('register.html', info=msg, this_uname=None)
            else:
                pending_user = PendingUser(email=this_email,
                                           code=verifyCode,
                                           firstname=this_firstname,
                                           lastname=this_lastname,
                                           user_pass=this_pass)
                db.session.add(pending_user)
                db.session.commit()
                return render_template("checkemail.html", this_uname=None)
        return render_template('register.html', info=msg, this_uname=None)
    return render_template('register.html', info=None, this_uname=None)


@app.route('/stock/<stockname>')
def stock(stockname):
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


@app.route('/check_email')
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


@app.route('/verify_email')
def verify_email():
    email = request.args.get('email')
    code = request.args.get('code')
    matches = PendingUser.query.filter(PendingUser.email == email)
    user = None
    for e in matches:
        if e.code == code:
            user = e

    if user is None:
        return redirect(url_for('index', message='Verification email expired'))

    # delete other pending users since accounts must have a unique email
    for e in matches:
        if e != user:
            db.session.delete(e)
    db.session.commit()

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
        if (e.get('name').upper().find(query) == 0
            or e.get('symbol').find(query) == 0):
            result.append(e)
            # limit results to 10 max
            if (len(result) == 10):
                break
    return jsonify(result)

@app.route('/sources')
def sources():
    return render_template('sources.html', this_uname=uname_getter())

@app.route('/about')
def about():
    return render_template('about.html', this_uname=uname_getter())


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
