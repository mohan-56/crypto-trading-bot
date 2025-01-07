# # src/main.py
# from exchange import Exchange
# from sentiment import SentimentAnalyzer
# from technical import TechnicalAnalyzer
# from strategy import TradingStrategy
# from config.config import CHECK_INTERVAL
# import time

# def run_bot():
#     print("Starting Crypto Trading Bot...")
#     exchange = Exchange()

#     sentiment_analyzer = SentimentAnalyzer()
#     technical_analyzer = TechnicalAnalyzer(exchange)
#     strategy = TradingStrategy(exchange, sentiment_analyzer, technical_analyzer)
    
#     while True:
       
#         try:
#             print("letsgooo")
#             # print("price"+"-----"+str(exchange.get_current_price()))
#             action, current_price = strategy.decide_trade()
#             result = strategy.execute_trade(action, current_price)
#             print(f"Price: {current_price}, Action: {result}")
#             time.sleep(CHECK_INTERVAL)
#         except Exception as e:
#             print(f"Error: {e}")
#             print("error in run bot.....")
#             time.sleep(60)

# if __name__ == "__main__":
#     run_bot()