from Models.Model import StockHoldings, User, db
from Services.layer2 import Stock_Service

def _get_cash_available(user):
    return user.balance


def _get_portfolio_value(holdings):
    value = 0
    for stock in holdings:
        value = value + stock.quantity * Stock_Service.get_stock_price(stock.stock_ticker)
    return value


def _get_all_investments(user):
    holdings = StockHoldings.query.filter(StockHoldings.person_id == user.id).all()
    return holdings

def get_portfolio(user):
    holdings = _get_all_investments(user)
    portfolioValue = _get_portfolio_value(holdings)
    cash = _get_cash_available(user)
    return cash, holdings, portfolioValue