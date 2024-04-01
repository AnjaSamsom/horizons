from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import csv
import yfinance as yf
import pandas as pd
import numpy as np
# adapted from A_random_walk_through_the_SP500_Python.ipynb

# stocks chosen
tickers = ['WMT','BRK-B','LEA','AEHR','AVGO','RYCEY','MTCH','FUN','TNL','AAL','XOM','META','TSLA','SCHW','M','COKE','AAPL','MRVL','JNJ','EADSY']

stock_prices = yf.download(tickers,start='2014-01-01')['Adj Close']     # Download the Daily Adjusted Close Price for the stocks
stock_prices = stock_prices.asfreq(freq='D',method='ffill')             # Change the dataframe to calendar day frequency and forward fill the prices for non trading days
stock_prices = stock_prices['2014-01-01':'2023-12-31'].fillna("bfill")  # If there are any remaining Naan, backfill with last available price
stock_returns = stock_prices.pct_change().fillna(0)                     # Create dataframe of stock returns and fill Naan with 0
stock_prices_normal = stock_prices / stock_prices.iloc[0]               # Create a dataframe of normalized prices

stocks = yf.Tickers(tickers)
company_names = {}
company_summary = {}
company_industry = {}
company_sector = {}
company_marketCap = {}

#collect information about each stock
for i in tickers:
  name_i = {i:stocks.tickers[i].info['longName']}
  summary_i = {i:stocks.tickers[i].info['longBusinessSummary']}
  industry_i = {i:stocks.tickers[i].info['industry']}
  sector_i = {i:stocks.tickers[i].info['sector']}
  marketCap_i = {i:stocks.tickers[i].info['marketCap']}
  company_names.update(name_i)
  company_summary.update(summary_i)
  company_industry.update(industry_i)
  company_sector.update(sector_i)
  company_marketCap.update(marketCap_i)

df1 = pd.DataFrame.from_dict(company_names, orient='index', columns=['Company Name'])
df2 = pd.DataFrame.from_dict(company_summary, orient='index', columns=['Business Summary'])
df3 = pd.DataFrame.from_dict(company_sector, orient='index', columns=['Sector'])
df4 = pd.DataFrame.from_dict(company_industry, orient='index', columns=['Industry'])
df5 = pd.DataFrame.from_dict(company_marketCap, orient='index', columns=['Market Cap'])
stock_info = df1.merge(right=df2, how='inner',left_index=True, right_index=True)
stock_info = stock_info.merge(right=df3, how='inner',left_index=True, right_index=True)
stock_info = stock_info.merge(right=df4, how='inner',left_index=True, right_index=True)
stock_info = stock_info.merge(right=df5, how='inner',left_index=True, right_index=True)

benchmark_prices = yf.download("^GSPC", start='2013-10-01')["Adj Close"] # Repeat previous steps, but now for benchmark
benchmark_prices = benchmark_prices.asfreq(freq='D',method='ffill')
benchmark_prices = benchmark_prices['2013-10-01':'2023-09-30']
benchmark_returns = benchmark_prices.pct_change().fillna(0)
benchmark_prices_normal = benchmark_prices / benchmark_prices.iloc[0]

stock_weights_equal = np.repeat(0.05,20)
mu = expected_returns.mean_historical_return(stock_prices)
Sigma = risk_models.sample_cov(stock_prices)

# use the efficient frontier to determine the best split of stocks
ef = EfficientFrontier(mu, Sigma, weight_bounds=(0.02,.10))
ef.max_sharpe()

# starting prices determined by sharpe ratio 
stock_weights_sharpe = dict(ef.clean_weights())
print(ef.portfolio_performance(verbose=True))

# write starting prices to a csv
with open('start.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for stock in stock_weights_sharpe.items():
    writer.writerow(stock)

stocks_equal = stock_prices_normal * stock_weights_equal * 10000
stocks_equal['Portfolio'] = stocks_equal.sum(axis=1)
stocks_equal['Benchmark'] = benchmark_prices_normal * 10000

stocks_sharpe = stock_prices_normal * stock_weights_sharpe * 10000
stocks_sharpe['Portfolio'] = stocks_sharpe.sum(axis=1)
stocks_sharpe['Benchmark'] = benchmark_prices_normal * 10000

# print the resultant weights
print("Resultant weights:")
print((stocks_equal.div(stocks_equal['Portfolio'], axis=0)).iloc[-1,0:20])
results = (stocks_equal.div(stocks_equal['Portfolio'], axis=0)).iloc[-1,0:20]
print(type(results.to_dict()))

results = results.to_dict()

with open('end.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  for stock in results.items():
    writer.writerow(stock)