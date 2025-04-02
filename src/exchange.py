# src/exchange.py
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import ccxt
from config.config import API_KEY, SECRET_KEY, SYMBOL, AMOUNT, API_PASSWORD

class Exchange:
    def __init__(self):
        self.exchange = ccxt.bitget({
            'apiKey': API_KEY,
            'secret': SECRET_KEY,
            'password': API_PASSWORD,
            'enableRateLimit': True,
            'timeout': 60000,  # 60 seconds
            'options': {
                'defaultType': 'spot',
                'createMarketBuyOrderRequiresPrice': False
            }
        })
        print("EXCHANGE:------->>>>>", self.exchange.id)
        self.load_markets_with_retry()

    def load_markets_with_retry(self, retries=5, delay=10):
        attempt = 0
        while attempt < retries:
            try:
                self.exchange.load_markets()
                if SYMBOL not in self.exchange.markets:
                    raise ValueError(f"Symbol {SYMBOL} not supported by Bitget spot.")
                print(f"Markets loaded successfully for {SYMBOL}")
                return
            except ccxt.RequestTimeout as e:
                attempt += 1
                print(f"Timeout loading markets (attempt {attempt}/{retries}): {e}")
                if attempt == retries:
                    raise Exception("Failed to load markets after all retries.")
                time.sleep(delay)
            except Exception as e:
                print(f"Unexpected error loading markets: {e}")
                raise

    def get_current_price(self):
        try:
            ticker = self.exchange.fetch_ticker(SYMBOL)
            print(f"Current Price: {ticker['last']}")
            return ticker['last']
        except Exception as e:
            print(f"Error fetching ticker: {e}")
            return None
    
    def fetch_ohlcv(self, timeframe='1h', limit=100, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                ohlcv = self.exchange.fetch_ohlcv(SYMBOL, timeframe=timeframe, limit=limit)
                if not ohlcv:
                    print(f"OHLCV data empty for {SYMBOL}. Retrying... ({attempt + 1}/{retries})")
                    attempt += 1
                    time.sleep(5)
                    continue
                print(f"Fetched {len(ohlcv)} OHLCV candles for {SYMBOL}")
                return ohlcv
            except Exception as e:
                print(f"Error fetching OHLCV: {e}")
                attempt += 1
                time.sleep(5)
        print(f"Failed to fetch OHLCV after {retries} attempts.")
        return []

    def get_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            btc_free = balance['BTC']['free'] if 'BTC' in balance else 0
            print(f"Available BTC balance: {btc_free}")
            return btc_free
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0

    def buy(self):
        try:
            order = self.exchange.create_market_buy_order(SYMBOL, AMOUNT)
            print(f"Buy order executed: {order}")
            return order
        except Exception as e:
            print(f"Error executing buy order: {e}")
            return None
    
    def sell(self, amount): 
        try:
            order = self.exchange.create_market_sell_order(SYMBOL, amount)
            print(f"Sell order executed: {order}")
            return order
        except Exception as e:
            print(f"Error executing sell order: {e}")
            return None