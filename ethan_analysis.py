import yfinance as yf
import pandas as pd
import json

def fetch_and_save_stock_data(tickers):
    # Create a dictionary to store various DataFrames for each stock
    stocks_data = {}

    for ticker in tickers:
        # Fetch historical data for the ticker
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")

        # Calculate additional metrics
        hist['Returns'] = hist['Close'].pct_change().fillna(0)
        hist['Normalized'] = hist['Close'] / hist['Close'].iloc[0]

        # Fetch additional stock info
        info = stock.info
        additional_info = {
            'longName': info.get('longName'),
            'sector': info.get('sector'),
            'fullTimeEmployees': info.get('fullTimeEmployees'),
            'marketCap': info.get('marketCap')
            # Add other info fields as required
        }

        # Convert dates to a string format
        hist.reset_index(inplace=True)
        hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')

        # Combine history with additional info
        combined_data = {
            'history': hist.to_dict(orient='records'),
            'info': additional_info
        }
        stocks_data[ticker] = combined_data

    # Save all data to a JSON file
    with open('stocks_data.json', 'w') as f:
        json.dump(stocks_data, f)

# Example usage
fetch_and_save_stock_data(["AAPL", "MSFT", "GOOGL"])
