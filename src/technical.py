# # src/technical.py
# import pandas as pd
# from ta.volatility import BollingerBands

# class TechnicalAnalyzer:
#     def __init__(self, exchange):
#         self.exchange = exchange
    
#     def get_technical_data(self):
#         ohlcv = self.exchange.fetch_ohlcv()
#         print("old Data -->",ohlcv)
#         df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
#         df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
#         bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2)
#         df['bb_upper'] = bb_indicator.bollinger_hband()
#         df['bb_lower'] = bb_indicator.bollinger_lband()
#         df['bb_middle'] = bb_indicator.bollinger_mavg()
        
#         return df