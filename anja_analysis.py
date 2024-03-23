import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def invest_10000(ticker):
    stock_prices = yf.download(ticker, start="2014-01-01", end="2023-12-31")["Adj Close"]
    stock_prices = stock_prices.asfreq(freq="D", method="bfill")
    stock_returns= stock_prices.pct_change()
    stock_returns_cumulative = (stock_returns+1).cumprod()
    stock_returns_cumulative
    stock_invest_10000 = 10000*stock_returns_cumulative
    print(stock_invest_10000)
    stock_invest_10000.plot(title= ticker + ": Value of $10,000 invested on January 1, 2014", figsize=(15,10))
    plt.savefig("css/images/" + ticker + "_invest_10000.png")
    plt.close()

tickers = ["RYCEY", "MTCH", "FUN", "TNL", "AAL"]
for ticker in tickers:
    invest_10000(ticker)

