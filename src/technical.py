
import pandas as pd
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

class TechnicalAnalyzer:
    def __init__(self, exchange):
        self.exchange = exchange
    
    def get_technical_data(self):
        ohlcv = self.exchange.fetch_ohlcv()
        print("old Data -->",ohlcv)
        if not ohlcv:
            print("No OHLCV data available. Returning empty DataFrame.")
            return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # print(" Data -->",df)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=1.5)
        df['bb_upper'] = bb_indicator.bollinger_hband()
        df['bb_lower'] = bb_indicator.bollinger_lband()
        df['bb_middle'] = bb_indicator.bollinger_mavg()

        rsi_indicator = RSIIndicator(close=df['close'], window=14)
        df['rsi'] = rsi_indicator.rsi()
        
        return df