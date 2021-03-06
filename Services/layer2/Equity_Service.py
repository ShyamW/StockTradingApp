from Models.Model import StockHoldings
from decimal import Decimal

def _valid_sell_(quantity, person, ticker):
    """ Determines if sell is valid
        Args:
            quantity: quantity of stock
            person: user buying equity
            ticker: stock ticker
        Returns:
            db entry if valid sell: else return false
        """
    # if quantity is not a value: error out
    try:
        quantity = int(quantity)
    except ValueError:
        return False

    result = StockHoldings.query.filter(StockHoldings.person_id == person.id,
                                        StockHoldings.stock_ticker == ticker).first()
    # if not owned or not enough owned: error out
    if not result or result.quantity < quantity or result.quantity is 0:
        return False

    return result


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
        old_quantity = result.quantity
        # update avg cost
        stock_price = Decimal(stock_price)
        result.avg_cost = (result.avg_cost * old_quantity + stock_price * quantity) / (old_quantity + quantity)
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
    result = _valid_sell_(quantity, person, ticker)
    if not result:
        return True

    quantity = int(quantity)

    # if selling all shares
    if result.quantity == quantity:
        db.session.delete(result)
        db.session.commit()

    # if partial sell
    else:
        result.quantity -= quantity
        db.session.commit()

    return False


