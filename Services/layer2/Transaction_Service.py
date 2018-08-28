import datetime
from Models.Model import StockTransactions


def record_buy(person, ticker, quantity, stock_price, db):
    """ Service to record a buy transaction
    Args:
        person: user buying equity
        ticker: stock ticker
        quantity: quantity of stock
        stock_price: price of stock to buy
        db: database instance
    """
    # add buy transaction to transactions table """
    buy_transaction = StockTransactions(person_id=person.id, stock_ticker=ticker, quantity=quantity,
                                    date=datetime.datetime.now(), avg_cost=stock_price)
    db.session.add(buy_transaction)
    db.session.commit()


def record_sell(person, ticker, quantity, stock_price, db):
    """ Service to record a sell transaction
    Args:
        person: user buying equity
        ticker: stock ticker
        quantity: quantity of stock
        stock_price: price of stock to buy
        db: database instance
    """
    # add sell transaction to transactions table """
    sell_transaction = StockTransactions(person_id=person.id, stock_ticker=ticker, quantity=quantity,
                                     date=datetime.datetime.now(), avg_cost=stock_price)
    db.session.add(sell_transaction)
    db.session.commit()


