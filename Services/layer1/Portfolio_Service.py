from Models.Model import StockHoldings, User, db
from Services.layer2 import Stock_Service
from decimal import Decimal


def _get_cash_available(user):
    """
    Gets the balance i
    Args:
         user: user for whom you want to get balance for.
    Returns:
        The balance of the account for the given user.
    """
    return user.balance


def _get_portfolio_value(holdings):
    """
        Args:
            holdings:
        Returns:
            The portfolio value, total of all the investments.
    """
    value = 0
    for stock in holdings:
        value = value + stock.quantity * Stock_Service.get_stock_price(stock.stock_ticker)
    return Decimal(value)


def _get_all_investments(user):
    """
    Args:
         user: user for whom you want to retrieve all the investments for.
    Returns:
         all the holdings of the given person, returned as a list.
    """
    holdings = StockHoldings.query.filter(StockHoldings.person_id == user.id).all()
    return holdings


def get_portfolio(user):
    """
    Args:
        user:
    Returns:
        a triplet of bank balance, list of holdings, and the portfolio value as of today.
    """
    holdings = _get_all_investments(user)
    portfolio_value = _get_portfolio_value(holdings)
    cash = _get_cash_available(user)
    total = cash + portfolio_value
    return holdings, cash, portfolio_value, total
