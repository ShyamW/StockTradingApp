from Models.Model import StockHoldings, User, db
from Services.layer2 import Stock_Service
from decimal import Decimal

def _get_cash_available(user):
    return user.balance


def _get_portfolio_value(holdings):
    value = 0
    for stock in holdings:
        value = value + stock.quantity * Stock_Service.get_stock_price(stock.stock_ticker)
    return Decimal(value)


def _get_all_investments(user):
    holdings = StockHoldings.query.filter(StockHoldings.person_id == user.id).all()
    return holdings

def get_portfolio(user):
    holdings = _get_all_investments(user)
    portfolio_value = _get_portfolio_value(holdings)
    cash = _get_cash_available(user)
    total = cash + portfolio_value
    return holdings, cash, portfolio_value, total
