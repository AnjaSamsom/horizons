import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from financetoolkit import Toolkit

from api_call import companies


def set_up(tickers):
    stock_prices = yf.download(tickers, start="2014-01-01", end="2023-12-31")["Adj Close"]
    stock_prices = stock_prices.asfreq(freq="D", method="ffill")
    stock_returns = stock_prices.pct_change()
    stock_returns.iloc[0]=0
    stock_returns_cumulative = (stock_returns+1).cumprod()
    stocks = yf.Tickers(tickers)
    return [stock_prices, stock_returns, stock_returns_cumulative, stocks]


def invest_10000(stock_returns_cumulative):
    stock_invest_10000 = 10000*stock_returns_cumulative
    stock_invest_10000.plot(title= "Value of $10,000 invested on January 1, 2014", figsize=(15,10))
    plt.savefig("css/images/graphs/invest_10000.png")
    plt.close()

def cagr(data, periods):
    final_value = data.iloc[-1]
    starting_value = data.iloc[0]
    N = periods
    (((final_value/starting_value)**(1/N))-1).to_csv("cagr"+str(periods)+".csv")
    return (((final_value/starting_value)**(1/N))-1)

def financial_metrics(tickers, companies):
    # total operating expenses
    income_statement = companies.get_income_statement()
    balance_sheet_statement = companies.get_balance_sheet_statement()
    profitability_ratios = companies.ratios.collect_profitability_ratios()
    valuation_ratios = companies.ratios.collect_valuation_ratios()

    for ticker in tickers:
        dates = [2019, 2020, 2021, 2022, 2023]

        #revenue
        data = income_statement.loc[ticker].loc["Revenue"]
        revenue = data.tolist()
        revenue = [x / 1000000000 for x in revenue]
        plt.plot(dates, revenue)
        plt.xticks(dates)
        plt.xlabel("Year")
        plt.ylabel("Revenue in Billion $")
        plt.title(stocks.tickers[ticker].info["longName"] + " Total Revenue")
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.savefig("css/images/graphs/revenue_" + ticker + ".png")
        plt.close()

         #operating expenses
        data = income_statement.loc[ticker].loc["Operating Expenses"]
        expenses = data.tolist()
        expenses = [x / 1000000000 for x in expenses]
        plt.plot(dates, expenses)
        plt.xticks(dates)
        plt.xlabel("Year")
        plt.ylabel("Total Operating Expenses in Billion $")
        plt.title(stocks.tickers[ticker].info["longName"] + " Operating Expenses")
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.savefig("css/images/graphs/operating_expenses_" + ticker + ".png")
        plt.close()
 
        # EBITDA
        data = income_statement.loc[ticker].loc["EBITDA"]
        EBITDA = data.tolist()
        EBITDA = [x / 1000000000 for x in EBITDA]
        dates = [2019, 2020, 2021, 2022, 2023]
        plt.plot(dates, EBITDA)
        plt.xticks(dates)
        plt.xlabel("Year")
        plt.ylabel("Total EBITDA in Billion $")
        plt.title(stocks.tickers[ticker].info["longName"] + " EBITDA")
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.savefig("css/images/graphs/EBITDA_" + ticker + ".png")
        plt.close()

        valuation_ratios.transpose()[ticker,'Earnings per Share'].plot(title=(stocks.tickers[ticker].info["longName"] + " Earnings per Share"))
        plt.savefig("css/images/graphs/EPS_" + ticker + ".png")
        plt.xlabel("Year")
        plt.ylabel("Earnings per Share ($)")
        plt.close()

        valuation_ratios.transpose()[ticker, "Price-to-Earnings"].plot(title=(stocks.tickers[ticker].info["longName"] + " Price/Earnings Ratio"))
        plt.savefig("css/images/graphs/PE_" + ticker + ".png")
        plt.xlabel("Year")
        plt.ylabel("Price to Earnings ($)")
        plt.close()

def correlation():
    stock_prices.corr().to_csv("corr.csv")
    print(stock_prices.corr())


tickers = ["RYCEY", "MTCH", "FUN", "TNL", "AAL"]
results = set_up(tickers)
stock_prices = results[0]
stock_returns = results[1]
stock_returns_cumulative = results[2]
stocks = results[3]
#invest_10000(stock_returns_cumulative)
toolkit_companies = companies
#financial_metrics(tickers, toolkit_companies)


#10 yr
ten_yrs = cagr(stock_prices["2014-01-01":"2023-12-31"], 10)

#5 yr
five_yrs = cagr(stock_prices["2019-01-01":"2023-12-31"], 5)

#3 yr
three_yrs = cagr(stock_prices["2021-01-01":"2023-12-31"], 3)

#1 yr
one_yr = cagr(stock_prices["2023-01-01":"2023-12-31"], 1) 




