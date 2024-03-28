import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from financetoolkit import Toolkit



def set_up(tickers):
    stock_prices = yf.download(tickers, start="2014-01-01", end="2023-12-31")["Adj Close"]
    stock_prices = stock_prices.asfreq(freq="D", method="ffill")
    stock_returns = stock_prices.pct_change()
    stock_returns.iloc[0]=0
    stock_returns_cumulative = (stock_returns+1).cumprod()
    return [stock_prices, stock_returns, stock_returns_cumulative]

def invest_10000(stock_returns_cumulative):
    stock_invest_10000 = 10000*stock_returns_cumulative
    stock_invest_10000.plot(title= "Value of $10,000 invested on January 1, 2014", figsize=(15,10))
    plt.savefig("css/images/invest_10000.png")
    plt.close()

def cagr(data, periods):
    final_value = data.iloc[-1]
    starting_value = data.iloc[0]
    N = periods
    return (((final_value/starting_value)**(1/N))-1)

def financial_metrics(tickers):
    # total revenue
    companies = Toolkit(tickers, api_key="NMm60KVgLfxxlqG2DQR6M4g2EtrF7GIz", start_date='2018-12-31')
    balance_sheet_statement = companies.get_balance_sheet_statement()
    income_statement = companies.get_income_statement()
    for ticker in tickers:
        print(income_statement.loc[ticker])
        df = income_statement.loc[ticker].loc[0:2]
        print(df)

        #plt.scatter(x, y, marker='o',label='Data')
        #plt.show()

    




tickers = ["RYCEY", "MTCH", "FUN", "TNL", "AAL"]
results = set_up(tickers)
stock_prices = results[0]
stock_returns = results[1]
stock_returns_cumulative = results[2]
invest_10000(stock_returns_cumulative)

#10 yr
ten_yrs = cagr(stock_prices["2014-01-01":"2023-12-31"], 10)

#5 yr
five_yrs = cagr(stock_prices["2019-01-01":"2023-12-31"], 5)

#3 yr
three_yrs = cagr(stock_prices["2021-01-01":"2023-12-31"], 3)

#1 yr
one_yr = cagr(stock_prices["2023-01-01":"2023-12-31"], 1)

financial_metrics(tickers)



