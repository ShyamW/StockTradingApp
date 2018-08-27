import requests
from pandas.io.json import json_normalize, loads
import pandas as pd
""" Service involving stock data """


def _build_url(ticker):
    """Builds URL for yahoo finance
    Args:
        ticker: stock ticker
    returns:
        price of stock"""
    end_seconds = int(pd.Timestamp("now").timestamp())
    start_seconds = 7223400
    site = "https://finance.yahoo.com/quote/" + ticker + "/history?period1=" + str(
        int(start_seconds)) + "&period2=" + \
           str(end_seconds) + "&interval=1d&filter=history&frequency=1d"
    return site


def _get_data(ticker):
    """Downloads historical stock price data into a pandas data frame
    Args:
        ticker: stock ticker
    returns:
        price of stock"""
    site = _build_url(ticker)
    resp = requests.get(site)
    html = resp.content.decode()
    start = html.index('"HistoricalPriceStore"')
    end = html.index("firstTradeDate")
    needed = html[start:end]
    needed = needed.strip('"HistoricalPriceStore":').strip(""","isPending":false,'""") + "}"
    temp = loads(needed)
    result = json_normalize(temp['prices'])
    return result[["date", "open", "high", "low", "close", "adjclose", "volume"]]['adjclose'][0]


def get_stock_price(ticker):
    """ Gets the stock price for ticker
    Args"
        ticker: stock ticker
    returns:
        price of stock"""
    stock_price = _get_data(ticker)
    return round(stock_price, 2)
