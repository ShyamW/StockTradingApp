from Services.layer2 import Stock_Service, Fund_Service
from flask import redirect, render_template

def buy(ticker, quantity, person):
    """ Service to buy a stock
    Args:
        ticker: stock ticker
        quantity: number of stocks to buy
        person: person that chooses to sell stock
    Returns:
        Success or Error Page """
    stock_price = Stock_Service.get_stock_price(ticker)
    total_price = quantity * stock_price

    """ if insufficient funds render warning """
    if person.balance < total_price:
        return render_template('buy_stock.html', ticker=ticker, stock_price=stock_price, failure=True, cost=total_price, cash_value=person.balance)

    Fund_Service.remove_funds(total_price, person)
    # TODO add buy transaction to transactions table and holdings table"""
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
    return '/stocks/show/' + ticker + '/'


