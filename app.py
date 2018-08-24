from flask import Flask, render_template, redirect, url_for, request
from Services.layer1.Stock_Service import StockService

""" declare services """
stock_service = StockService()

app = Flask(__name__)


"""TODO:CODY NEED LOGIN HERE"""


""" This is Core Funx """


"""
Welcome Page to view portfolio and stocks
"""
@app.route('/')
def landing():
    return redirect(url_for('welcome'))
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

""" Redirects from Users Search to show_stock"""
@app.route('/stocks/show/')
def redir_show():
    ticker = request.args.get('ticker')
    return redirect('/stocks/show/' + ticker + '/')

""" Shows Stock data for <ticker>
Params:
    ticker: ticker value for stock """
@app.route('/stocks/show/<ticker>/')
def show_stock(ticker):
    return render_template('show_stock.html', ticker=ticker, stock_price=stock_service.get_stock_price(ticker))





""" 
Buy and Sell Stocks 
"""
""" Buys a stock if funds
Params:
    ticker: ticker value for stock """
@app.route('/stocks/show/<ticker>/Buy/')
def buy_stock(ticker):
    stock_price = stock_service.get_stock_price(ticker)
    return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price)

""" Sells a stock if funds
Params:
    ticker: ticker value for stock """
@app.route('/stocks/show/<ticker>/Sell/')
def sell_stock(ticker):
    stock_price = stock_service.get_stock_price(ticker)
    return render_template('sell_stock.html', ticker=ticker, stock_price=stock_price)

if __name__ == '__main__':
    app.run()
