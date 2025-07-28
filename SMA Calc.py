import pandas as pd
import yfinance as yf

def get_data(ticker, start_date, end_date):
    """
    Function to retrieve historical stock data using Yahoo Finance API.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_indicators(data):
    """
    Function to calculate moving averages for the stock data.
    """
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    return data

def main():
    # Input stock symbol
    ticker = input("Enter the stock symbol: ").upper()

    # Define parameters
    start_date = '2023-1-1'
    end_date = '2024-4-13'

    # Retrieve data
    try:
        stock_data = get_data(ticker, start_date, end_date)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Calculate indicators
    stock_data = calculate_indicators(stock_data)

    # Display SMA values
    last_row = stock_data.iloc[-1]
    sma_50 = last_row['SMA_50']
    sma_200 = last_row['SMA_200']

    print(f"50-day SMA for {ticker}: {sma_50}")
    print(f"200-day SMA for {ticker}: {sma_200}")

if __name__ == "__main__":
    main()