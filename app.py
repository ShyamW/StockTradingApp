from flask import Flask, render_template, redirect, url_for, request, flash

# Services
from Services.layer1 import Order_Service, Banking_Service
from Services.layer2 import Stock_Service

""" Controller Class """
app = Flask(__name__)
# App config.
DEBUG = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


person = "bob"


@app.route('/')
def landing():
    """
    Root Page. Force Login, then after login: redirect to welcome page
    """
    return redirect(url_for('welcome'))


@app.route('/welcome')  # TODO; get total portfolio value, cash value, stock value, stock breakdown
def welcome():
    """
    Welcome Page to view portfolio and stocks
    """
    return render_template('welcome.html')


@app.route('/bank/', methods=["GET", "POST"])
def bank():
    """
    Bank Page to do transfers
    """
    if request.method == 'POST':
        Banking_Service.transfer_money(request, person)
    cash_value = 0
    name = 'jon'
    return render_template('bank.html', cash_value=cash_value, name=name)


"""--------------------------------------   Buying and Selling Stock ------------------------------------------------"""


@app.route('/stocks/show/<ticker>/Buy/', methods=["GET", "POST"])
def buy_stock(ticker):
    """ Buys a stock if funds
    Params:
        ticker: ticker value for stock """
    # if buying a stock
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        url = Order_Service.buy(ticker, quantity, person)
        return redirect(url)
    else:  # if getting the buy page
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price)


@app.route('/stocks/show/<ticker>/Sell/', methods=["GET", "POST"])
def sell_stock(ticker):
    """ Sells a stock if funds
    Params:
        ticker: ticker value for stock """
    # if selling a stock
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        url = Order_Service.sell(ticker, quantity, person)
        return redirect(url)
    else:
        stock_price = Stock_Service.get_stock_price(ticker)
        return render_template('sell_stock.html', ticker=ticker, stock_price=stock_price)


"""-------------------------------------------   Viewing A stock ----------------------------------------------------"""


@app.route('/stocks/show/')
def redirect_show():
    """ Redirects to show_stock when user searches specific stock """
    ticker = request.args.get('ticker')
    return redirect('/stocks/show/' + ticker + '/')


@app.route('/stocks/show/<ticker>/')
def show_stock(ticker):
    """ Shows Stock data for <ticker>
    Params:
        ticker: ticker symbol for stock """
    stock_price = Stock_Service.get_stock_price(ticker)
    return render_template('show_stock.html', ticker=ticker, stock_price=stock_price)


if __name__ == '__main__':
    app.run()
