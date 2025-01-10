# src/strategy.py
from config.config import SENTIMENT_BUY_THRESHOLD, SENTIMENT_SELL_THRESHOLD, DCA_THRESHOLD,AMOUNT

class TradingStrategy:
    def __init__(self, exchange, sentiment_analyzer, technical_analyzer):
        self.exchange = exchange
        self.sentiment_analyzer = sentiment_analyzer
        self.technical_analyzer = technical_analyzer
        self.holdings = 0
        self.avg_price = 0
    
    def dca_strategy(self, current_price):
        if self.holdings > 0 and current_price < self.avg_price * DCA_THRESHOLD:
            return "buy"
        return "hold"
    
    def decide_trade(self):
        current_price = self.exchange.get_current_price()
        sentiment = self.sentiment_analyzer.get_sentiment()
        df = self.technical_analyzer.get_technical_data()
        # print(df)
        if df is None or df.empty:
            print("No technical data available.")
            return "hold", current_price
        latest = df.iloc[-1]
        
        action = "hold"
        
        # Sentiment-based decision
        if sentiment > SENTIMENT_BUY_THRESHOLD:
            action = "buy"
            print("going moooon")
        elif sentiment < SENTIMENT_SELL_THRESHOLD:
            action = "sell"
            print("lets fill our pockets")
        
        # Bollinger Bands override
        if current_price > latest['bb_upper']:
            action = "sell"
            print("selling")
        elif current_price < latest['bb_lower']:
            action = "buy"
            print("buying")
        
        # DCA adjustment
        if self.holdings > 0:
            action = self.dca_strategy(current_price)
        
        return action, current_price
    
    def execute_trade(self, action, current_price):
        if action == "buy":
            self.exchange.buy()
            prev_holdings = self.holdings
            self.holdings += AMOUNT
            self.avg_price = (self.avg_price * prev_holdings + current_price * AMOUNT) / self.holdings
            return f"BUY: {AMOUNT} BTC at {current_price}, Holdings: {self.holdings}"
        
        elif action == "sell" and self.holdings >= AMOUNT:
            self.exchange.sell()
            self.holdings -= AMOUNT
            profit = (current_price - self.avg_price) * AMOUNT
            return f"SELL: {AMOUNT} BTC at {current_price}, Profit: {profit}"
        
        return "HOLD: No action taken"