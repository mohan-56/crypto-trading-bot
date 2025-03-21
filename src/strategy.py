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
            print(f"DCA: Price {current_price} < Avg {self.avg_price * DCA_THRESHOLD}")
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
        
        print(f"BB - Upper: {latest['bb_upper']:.2f}, Lower: {latest['bb_lower']:.2f}, Middle: {latest['bb_middle']:.2f}")
        
        action = "hold"
        
        # Sentiment-based decision
        if sentiment > SENTIMENT_BUY_THRESHOLD:
            print(f"Sentiment {sentiment} > Buy Threshold {SENTIMENT_BUY_THRESHOLD}: Setting action to buy")
            action = "buy"
            print("going moooon")
        elif sentiment < SENTIMENT_SELL_THRESHOLD:
            print(f"Sentiment {sentiment} < Sell Threshold {SENTIMENT_SELL_THRESHOLD}: Setting action to sell")
            action = "sell"
            print("lets fill our pockets")
        
        # Bollinger Bands override
        if current_price > latest['bb_upper']:
            print(f"Price {current_price} > BB Upper {latest['bb_upper']}: Setting action to sell")
            action = "sell"
            print("selling")
        elif current_price < latest['bb_lower']:
            print(f"Price {current_price} < BB Lower {latest['bb_lower']}: Setting action to buy")
            action = "buy"
            print("buying")
        
        # DCA adjustment
        if self.holdings > 0:
            action = self.dca_strategy(current_price)
        
        return action, current_price
    
    def execute_trade(self, action, current_price):
        if current_price is None:
            return "HOLD: No price data available"
        # action="sell"
        if action == "buy":
           
            order = self.exchange.buy()
            if order:
                btc_amount = AMOUNT / current_price  # Convert USDT cost to BTC
                prev_holdings = self.holdings
                self.holdings += btc_amount
                self.avg_price = (self.avg_price * prev_holdings + current_price * btc_amount) / self.holdings
                return f"BUY: {btc_amount:.6f} BTC at {current_price}, Holdings: {self.holdings:.6f}"
            print("Buy failed - check funds or API permissions")
            return "HOLD: Buy failed"
        
        elif action == "sell" and self.holdings >= AMOUNT:
           
            sell_amount = min(self.holdings, AMOUNT / current_price)  # Sell up to holdings or AMOUNT’s BTC equivalent
            order = self.exchange.sell(sell_amount)  # Pass calculated BTC amount
            if order:
                self.holdings -= sell_amount
                profit = (current_price - self.avg_price) * sell_amount
                return f"SELL: {sell_amount:.6f} BTC at {current_price}, Profit: {profit:.2f}"
            print("Sell failed - check holdings or API permissions")
            return "HOLD: Sell failed"
        
        return "HOLD: No action taken"