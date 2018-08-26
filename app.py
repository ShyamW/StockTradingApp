from flask import Flask, render_template, redirect, url_for, request, flash
from flask_user import login_required, UserManager, UserMixin
from Services.layer1 import Stock_Service
from Models.Model11 import db, User

""" Controller Class """
app = Flask(__name__)
# App config.
DEBUG = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# Flask-User settings
app.config['USER_APP_NAME'] = "Stock App"
app.config['USER_ENABLE_EMAIL'] = False  # No email authentication
app.config['USER_ENABLE_USERNAME'] = True  # Just use username auth
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True  # Make user retype password

# Set up Login Info
user_manager = UserManager(app, db, User)

#TODO
#Initialize Database here (method is in Models/Schemas.py)



@app.route('/')
def landing():
    """
    Root Page. Force Login, then after login: redirect to welcome page
    """
    # TODO; get total portfolio value, cash value, stock value, stock breakdown
    return redirect(url_for('welcome'))




@app.route('/welcome')
def welcome():
    """
    Welcome Page to view portfolio and stocks
    """
    return render_template('welcome.html')

@app.route('/bank')
def bank():
    """
    Bank Page to do transfers
    """
    cash_value = 0
    name = 'jon'
    return render_template('bank.html', cash_value=cash_value, name=name)

"""-------------------------------------------   Viewing A stock ----------------------------------------------------"""


@app.route('/stocks/show/')
def redir_show():
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


"""--------------------------------------   Buying and Selling Stock ------------------------------------------------"""

# TODO: write buy and sell services

@app.route('/stocks/show/<ticker>/Buy/', methods=["GET", "POST"])
def buy_stock(ticker):
    """
    Buy and Sell Stocks
    """
    """ Buys a stock if funds
    Params:
        ticker: ticker value for stock """
    stock_price = Stock_Service.get_stock_price(ticker)
    # if buying a stock
    if request.method == 'POST':
        quantity = request.form['quantity']
        print(quantity)
        flash("BOUGHT!!!")
        return redirect('/stocks/show/' + ticker + '/')
    # if getting the buy page
    else:
        return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price)


@app.route('/stocks/show/<ticker>/Sell/', methods=["GET", "POST"])
def sell_stock(ticker):
    """ Sells a stock if funds
    Params:
        ticker: ticker value for stock """
    stock_price = Stock_Service.get_stock_price(ticker)

    if request.method == 'POST':
        quantity = request.form['quantity']
        print(quantity)
        flash("SOLD!!!")
        return redirect('/stocks/show/' + ticker + '/')
    else:
        return render_template('sell_stock.html', ticker=ticker, stock_price=stock_price)


if __name__ == '__main__':
    app.run()
