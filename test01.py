import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

# load environment variables from .env
load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")

if not API_KEY or not API_SECRET:
    raise SystemExit("Missing ALPACA_API_KEY or ALPACA_API_SECRET in .env")

# paper=True ensures paper trading
client = TradingClient(API_KEY, API_SECRET, paper=True)

# Basic smoke test: account & positions
acct = client.get_account()
print("Account status:", acct.status)
print("Buying power:", acct.buying_power)

positions = client.get_all_positions()
print("Open positions:", [p.symbol for p in positions])
# TODO: fetch last trade for AAPL and print price/time
aapl_trade = client.get_latest_trade("AAPL")
print("AAPL latest trade:", aapl_trade.price, "at", aapl_trade.timestamp)

