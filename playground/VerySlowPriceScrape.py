# import stock_info module from yahoo_fin

from yahoo_fin import stock_info as si

price = si.get_live_price("AAPL")
print(price)


