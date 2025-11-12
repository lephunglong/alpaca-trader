#Read CSv file "Stocks to be detected.csv" to get stock list
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stock_list(file_path='Stocks to be detected.csv'):
    """Load the list of stock symbols from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df['Symbol'].tolist()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
stock_list = get_stock_list()

#for each stock in stock list, calculate its daily RSI of 14 days

def process_stock(symbol):
    try:
        rsi = calculate_rsi(symbol, period=14)
        if rsi is not None:
            print(f"Stock: {symbol}, RSI(14): {rsi}")
        else:
            print(f"Stock: {symbol}, RSI(14): Data not available")
    except Exception as e:
        print(f"Error processing {symbol}: {e}")

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_symbol = {executor.submit(process_stock, symbol): symbol for symbol in stock_list}
    for future in as_completed(future_to_symbol):
        symbol = future_to_symbol[future]
        try:
            future.result()
        except Exception as e:
            print(f"Error processing {symbol}: {e}")

#function to calculate RSI

def calculate_rsi(symbol, period=14):
    try:
        # Fetch historical data
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1mo")  # Fetch 1 month of data for RSI calculation
        if hist.empty or 'Close' not in hist:
            print(f"No historical data available for {symbol}")
            return None

        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]  # Return the latest RSI value
    except Exception as e:
        print(f"Error calculating RSI for {symbol}: {e}")
        return None


