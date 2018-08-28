from Models.Model import StockHoldings


def record_buy(person, ticker, quantity, stock_price, db):
    """ Service to record buying an equity
    Args:
        person: user buying equity
        ticker: stock ticker
        quantity: quantity of stock
        stock_price: stock_price
        db: database instance
    """
    # add bought stocks to stock holdings table"""
    result = StockHoldings.query.filter(StockHoldings.person_id == person.id,
                                        StockHoldings.stock_ticker == ticker).first()
    # if equity already owned: add quantity and update avg price
    if result:
        q = result.quantity
        result.avg_cost = (result.avg_cost * q + stock_price) / (q+1)  # update avg cost
        result.quantity += quantity
        db.session.commit()
    # else if equity is not held: add an entry for equity
    else:
        x = StockHoldings(person_id=person.id, stock_ticker=ticker, quantity=quantity, avg_cost=stock_price)
        db.session.add(x)
        db.session.commit()


def record_sell(person, ticker, quantity, db):
    """ Service to record selling an equity
    Args:
        person: user buying equity
        ticker: stock ticker
        quantity: quantity of stock
        db: database instance
    Returns:
        False if succeeded
    """
    result = StockHoldings.query.filter(StockHoldings.person_id == person.id,
                                        StockHoldings.stock_ticker == ticker).first()
    # if not owned or not enough owned: error out
    if not result or result.quantity < quantity:
        return True

    # if selling all shares
    elif result.quantity == quantity:
        db.session.delete(result)
        db.session.commit()

    # if partial sell
    else:
        result.quantity -= quantity
        db.session.commit()

    return False


