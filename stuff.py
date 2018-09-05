from flask import Flask, render_template, url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock', methods=['GET','POST'])
def stock():
    return render_template('stock.html')

@app.route('/page')
def page():
    return render_template('page.html')
