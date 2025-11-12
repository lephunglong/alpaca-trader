# Scan the stocks and return a list of stock symbols that meet Day RSI < 25 and Average Daily Volume > 6M
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import talib as ta
import logging
import time
import concurrent.futures
import os
from tqdm import tqdm
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def get_stock_list(file_path='Stocks to be detected.csv'):
    """Load the list of stock symbols from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df['Symbol'].tolist()
    except Exception as e:
        logging.error(f"Error loading stock list: {e}")
        return []
    
def fetch_stock_data(symbol, period='60d', interval='1d'):
    """Fetch historical stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        if hist.empty:
            logging.warning(f"No data found for {symbol}")
            return None
        return hist
    except Exception as e:
        logging.error(f"Error fetching data for {symbol}: {e}")
        return None
    
def calculate_rsi_and_volume(hist):
    """Calculate the Day RSI and Average Daily Volume."""
    try:
        close_prices = hist['Close'].values
        volumes = hist['Volume'].values
        rsi = ta.RSI(close_prices, timeperiod=14)
        avg_volume = np.mean(volumes)
        return rsi[-1], avg_volume
    except Exception as e:
        logging.error(f"Error calculating RSI and volume: {e}")
        return None, None
    
def scan_stocks(stock_list):
    """Scan stocks and return those that meet the criteria."""
    qualifying_stocks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_symbol = {executor.submit(process_stock, symbol): symbol for symbol in stock_list}
        for future in tqdm(concurrent.futures.as_completed(future_to_symbol), total=len(stock_list)):
            symbol = future_to_symbol[future]
            try:
                result = future.result()
                if result:
                    qualifying_stocks.append(result)
            except Exception as e:
                logging.error(f"Error processing stock {symbol}: {e}")
    return qualifying_stocks

def process_stock(symbol):
    """Process an individual stock to check if it meets the criteria."""
    hist = fetch_stock_data(symbol)
    if hist is None:
        return None
    rsi, avg_volume = calculate_rsi_and_volume(hist)
    if rsi is not None and avg_volume is not None:
        if rsi < 25 and avg_volume > 6_000_000:
            logging.info(f"Stock {symbol} meets criteria: RSI={rsi}, Avg Volume={avg_volume}")
            return symbol
    return None

if __name__ == "__main__":
    stock_list = get_stock_list()
    qualifying_stocks = []  # ensure the variable is always defined
    if not stock_list:
        logging.error("No stocks to scan.")
    else:
        result = scan_stocks(stock_list)
        qualifying_stocks = result if result else []
        logging.info(f"Qualifying stocks: {qualifying_stocks}")

# Save the qualifying stocks to a CSV file

output_df = pd.DataFrame(qualifying_stocks, columns=['Symbol'])
output_df.to_csv('qualifying_stocks.csv', index=False)





