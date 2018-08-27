from Services.layer2 import Stock_Service, Fund_Service
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from flask import redirect, render_template
from Models.Model import StockHoldings, StockTransactions
from app import db
import datetime


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
    if person.balance < total_price:
        return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price, failure=True, cost=total_price, cash_value=person.balance)

    Fund_Service.remove_funds(total_price, person)

    # add buy transaction to transactions table and holdings table"""
    x = StockHoldings(person_id=person.id, stock_ticker=ticker, quantity=quantity, avg_cost=stock_price)
    print(x)
    db.session.add(x)
    db.session.commit()

    y = StockTransactions(person_id=person.id, stock_ticker=ticker, quantity=quantity, date=datetime.datetime.now(), avg_cost=stock_price)
    print(y)
    db.session.add(y)

    db.session.commit()



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
    Fund_Service.add_funds(total_price, person)
    # TODO check they own the stocks and quantity, remove from holdings, add to transactions
    """ if user has enough stocks to sell, add total_price to user balance and add sell transaction to Transactions table"""
    """ else: return error"""
    # add buy transaction to transactions table and holdings table"""
    sell_order = StockHoldings(person_id=person.id, stock_ticker=ticker, quantity=quantity, avg_cost=stock_price)
    db.session.add(sell_order)

    sell_history = StockTransactions(person_id=person.id, stock_ticker=ticker, quantity=quantity, date=DateTime(timezone=True),
                              server_default=func.now(), avg_cost=stock_price)
    db.session.add(sell_history)

    db.session.commit()

    return '/stocks/show/' + ticker + '/'


