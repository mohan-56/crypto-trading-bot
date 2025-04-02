# telegram_bot.py
import sys
import os
import time
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.strategy import TradingStrategy
from src.exchange import Exchange
from src.sentiment import SentimentAnalyzer
from src.technical import TechnicalAnalyzer
from config.config import API_KEY, SECRET_KEY, API_PASSWORD, NEWS_API_KEY, BOT_KEY

# Initialize exchange and strategy
exchange = Exchange()
sentiment_analyzer = SentimentAnalyzer()
technical_analyzer = TechnicalAnalyzer(exchange)
strategy = TradingStrategy(exchange, sentiment_analyzer, technical_analyzer)

# Telegram API base URL
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_KEY}"

def send_message(chat_id, text):
    """Send a message to a Telegram chat."""
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)
        response.raise_for_status()
        print(f"Sent message to {chat_id}: {text}")
    except requests.RequestException as e:
        print(f"Error sending message: {e}")

def handle_update(update):
    """Process incoming Telegram updates."""
    if "message" not in update or "text" not in update["message"]:
        return
    
    chat_id = update["message"]["chat"]["id"]
    command = update["message"]["text"].strip()
    print(f"Received command from {chat_id}: {command}")  # Debug incoming messages

    if command == "/start":
        send_message(chat_id, "Welcome to CryptoTraderBot! Use /trade or /balance.")
    elif command == "/trade":
        action, current_price = strategy.decide_trade()
        result = strategy.execute_trade(action, current_price)
        send_message(chat_id, f"Trade Decision: {result}\nPrice: {current_price or 'N/A'}")
    elif command == "/balance":
        btc_balance = exchange.get_balance()
        send_message(chat_id, f"Current BTC Balance: {btc_balance:.8f}\nBot Holdings: {strategy.holdings:.8f}")
    else:
        send_message(chat_id, "Try /start, /trade, or /balance.")

def main():
    print("Telegram bot is running...")
    offset = None
    
    while True:
        try:
            url = f"{TELEGRAM_API}/getUpdates"
            params = {"timeout": 60, "offset": offset}
            response = requests.get(url, params=params, timeout=65)
            response.raise_for_status()
            data = response.json()

            if not data["ok"] or not data["result"]:
                print("No new updates.")
                time.sleep(1)
                continue

            for update in data["result"]:
                handle_update(update)
                offset = update["update_id"] + 1
                print(f"Processed update ID: {offset - 1}")

        except requests.RequestException as e:
            print(f"Polling error: {e}")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Bot stopped by user.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()