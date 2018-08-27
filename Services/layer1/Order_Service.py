from Services.layer2 import Stock_Service, Fund_Service


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
    Fund_Service.remove_funds(total_price, person)
    # TODO
    """ if user has enough money, subtract total_price from user balance and add buy transaction to transactions table"""
    """ else: return error"""
    return '/stocks/show/' + ticker + '/'


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
    # TODO
    """ if user has enough stocks to sell, add total_price to user balance and add sell transaction to Transactions table"""
    """ else: return error"""
    return '/stocks/show/' + ticker + '/'
