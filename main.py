import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestTradeRequest


# load environment variables from .env
load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")

if not API_KEY or not API_SECRET:
    raise SystemExit("Missing ALPACA_API_KEY or ALPACA_API_SECRET in .env")

# paper=True ensures paper trading
client = TradingClient(API_KEY, API_SECRET, paper=True)

# Basic smoke test: account &   
acct = client.get_account()
print("Account status:", acct.status)
print("Buying power:", acct.buying_power)

positions = client.get_all_positions()
print("Open positions:", [p.symbol for p in positions])

# TODO: fetch last trade for TSLA and print price/timestamp here
data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
latest_trade_request = StockLatestTradeRequest(symbol_or_symbols=["TSLA","NVDA"])
latest_trades = data_client.get_stock_latest_trade(latest_trade_request)
for symbol, trade in latest_trades.items():
    print(f"Latest trade for {symbol}: Price={trade.price}, Timestamp={trade.timestamp}")

     