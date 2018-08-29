from Services.layer2 import Stock_Service, Fund_Service, Transaction_Service, Equity_Service
from flask import redirect, render_template
from app import db


def buy(ticker, request_form, person):
    """ Service to buy a stock
    Args:
        ticker: stock ticker
        request_form: request param
        person: person that chooses to sell stock
    Returns:
        Success or Error Page """
    quantity = int(request_form.form['quantity'])
    stock_price = Stock_Service.get_stock_price(ticker)
    total_price = quantity * stock_price

    """ if insufficient funds render warning """
    if person.balance < total_price or quantity is 0:
        return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price, failure=True, cost=total_price,
                               cash_value=person.balance)

    Fund_Service.remove_funds(total_price, person)
    Equity_Service.record_buy(person, ticker, quantity, stock_price, db)
    Transaction_Service.record_buy(person, ticker, quantity, stock_price, db)
    return redirect('/stocks/show/' + ticker + '/')


def sell(ticker, quantity, person):
    """ Service to sell a stock
    Args:
        ticker: stock ticker
        quantity: number of stocks to buy
        person: person that chooses to sell stock
    Returns:
        Success or Error Page """
    stock_price = Stock_Service.get_stock_price(ticker)
    total_price = quantity * stock_price

    # if unable to sell equities: error out
    if Equity_Service.record_sell(person, ticker, quantity, db):
        return '/stocks/show/' + ticker + '/'

    Transaction_Service.record_sell(person, ticker, -quantity, stock_price, db)
    Fund_Service.add_funds(total_price, person)
    return '/stocks/show/' + ticker + '/'


