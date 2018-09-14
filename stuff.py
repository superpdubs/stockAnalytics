from flask import Flask, render_template, request, url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock', methods=['GET','POST'])
def stock():
    ticker = request.args['ticker'].upper();
    return render_template('stock.html', stock_name="Contoso Ltd.", stock_ticker=ticker, stock_value="XX.XX", stock_change="X.XX")

@app.route('/page')
def page():
    return render_template('page.html')