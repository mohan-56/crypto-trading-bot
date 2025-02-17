# src/exchange.py
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ccxt
from config.config import API_KEY, SECRET_KEY, SYMBOL, AMOUNT

class Exchange:
    def __init__(self):
        self.exchange = ccxt.bitget({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,
        })
        print("EXCHANGE:------->>>>>",self.exchange)
        # print(self.exchange.features)
    
    def get_current_price(self):
        ticker = self.exchange.fetch_ticker(SYMBOL)
        print(ticker)
        return ticker['last']
    
    def fetch_ohlcv(self, timeframe='1h', limit=100):
        return self.exchange.fetch_ohlcv(SYMBOL, timeframe, limit)
    
    def buy(self):
        order = self.exchange.create_market_buy_order(SYMBOL, AMOUNT)
        return order
    
    def sell(self):
        order = self.exchange.create_market_sell_order(SYMBOL, AMOUNT)
        return order