from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)


"""TODO NEED LOGIN HERE"""



""" This is Core Funx """
"""Welcome Page to view portfolio and stocks"""
@app.route('/')
def landing():
    return redirect(url_for('welcome'))
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

""" Redirects from Users Search to show_stock"""
@app.route('/show/')
def redir_show():
    ticker = request.args.get('ticker')
    return redirect('/show/' + ticker + '/')

""" Shows Stock data for <ticker>
Params:
    ticker: ticker value for stock """
@app.route('/show/<ticker>/')
def show_stock(ticker):
    return render_template('show_stock.html', SYMBOL=ticker)





""" Buy and Sell Stocks """

""" Buys a stock if funds
Params:
    ticker: ticker value for stock """
@app.route('/show/<ticker>/Buy/')
def buy_stock(ticker):
    return render_template('buy_stock.html', SYMBOL=ticker)

""" Sells a stock if funds
Params:
    ticker: ticker value for stock """
@app.route('/show/<ticker>/Sell/')
def sell_stock(ticker):
    return render_template('sell_stock.html', SYMBOL=ticker)

if __name__ == '__main__':
    app.run()
