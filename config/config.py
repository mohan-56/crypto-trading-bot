
SYMBOL = "BTC/USDT"
AMOUNT = 1.5  # Trading amount in USDT
CHECK_INTERVAL = 3600  # Seconds (1 hour)


import os
API_KEY = os.getenv("BITGET_API_KEY")
SECRET_KEY = os.getenv("BITGET_SECRET_KEY")
API_PASSWORD = os.getenv("BITGET_API_PASSWORD")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



# Trading thresholds
SENTIMENT_BUY_THRESHOLD = 0.2
SENTIMENT_SELL_THRESHOLD = -0.2
DCA_THRESHOLD = 0.98  # 2% drop for DCA