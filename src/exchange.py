# src/exchange.py
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ccxt
from config.config import API_KEY, SECRET_KEY, SYMBOL, AMOUNT
import time

class Exchange:
    def __init__(self):
        self.exchange = ccxt.bitget({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'enableRateLimit': True,
             'options': {
                'defaultType': 'spot',  # Explicitly set to spot trading
            }
        })
        print("EXCHANGE:------->>>>>",self.exchange)
        # print(self.exchange.features)

         # Load markets to ensure symbol is recognized
        self.exchange.load_markets()
        if SYMBOL not in self.exchange.markets:
            raise ValueError(f"Symbol {SYMBOL} not supported by Bitget. Check available markets.")
    
    def get_current_price(self):
        try:
            ticker = self.exchange.fetch_ticker(SYMBOL)
            return ticker['last']
        except Exception as e:
            print(f"Error fetching ticker: {e}")
            return None
    
    # def fetch_ohlcv(self, timeframe='1h', limit=100):
    #     return self.exchange.fetch_ohlcv(SYMBOL, timeframe, limit)
    def fetch_ohlcv(self, timeframe='1h', limit=100, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                ohlcv = self.exchange.fetch_ohlcv(SYMBOL, timeframe=timeframe, limit=limit)
                if not ohlcv:
                    print(f"OHLCV data empty for {SYMBOL}. Retrying... ({attempt + 1}/{retries})")
                    attempt += 1
                    time.sleep(5)  # Wait before retrying
                    continue
                print(f"Fetched {len(ohlcv)} OHLCV candles for {SYMBOL}")
                return ohlcv
            except Exception as e:
                print(f"Error fetching OHLCV: {e}")
                attempt += 1
                time.sleep(5)
        print(f"Failed to fetch OHLCV after {retries} attempts.")
        return []  # Return empty list if all retries fail
    
    def buy(self):
        try:
            order = self.exchange.create_market_buy_order(SYMBOL, AMOUNT)
            return order
        except Exception as e:
            print(f"Error executing buy order: {e}")
            return None
    
    def sell(self):
        try:
            order = self.exchange.create_market_sell_order(SYMBOL, AMOUNT)
            return order
        except Exception as e:
            print(f"Error executing sell order: {e}")
            return None