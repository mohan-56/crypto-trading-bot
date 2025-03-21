# Crypto Trading Bot

A Python-based automated trading bot for the Bitget exchange, utilizing sentiment analysis and technical indicators (Bollinger Bands) to execute buy and sell orders for BTC/USDT.

## Overview
This bot integrates:
- **Sentiment Analysis**: Fetches news from NewsAPI and uses TextBlob to gauge market sentiment.
- **Technical Analysis**: Calculates Bollinger Bands from hourly OHLCV data.
- **Trading Strategy**: Combines sentiment and technical signals, with Dollar-Cost Averaging (DCA) for risk management.
- **Exchange Integration**: Executes trades on Bitget via the CCXT library.

## Features
- Trades BTC/USDT based on sentiment scores and Bollinger Bands.
- Configurable thresholds for buying, selling, and DCA.
- Minimum trade size enforcement (0.000001 BTC) to comply with Bitget requirements.
- Error handling for insufficient balance and API issues.

## Prerequisites
- Python 3.8+
- Bitget account with API key, secret, and passphrase
- NewsAPI key
- Required libraries: `ccxt`, `pandas`, `ta`, `textblob`, `requests`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mohan-56/crypto-trading-bot.git
   cd crypto-trading-bot
2. Install dependencies:
   ```bash

   pip install -r requirements.txt



3. Configure the bot:
   Edit config/config.py with your API credentials:
   ```python
    

    API_KEY = "your_bitget_api_key"
    SECRET_KEY = "your_bitget_secret_key"
    API_PASSWORD = "your_bitget_api_passphrase"
    NEWS_API_KEY = "your_newsapi_key"

## Usage
  1. Run the bot:
       ```bash
         python src/main.py

2. Monitor the console output for trading decisions and execution logs.
   The bot checks conditions every 3600 seconds (1 hour) by default (adjustable in config.py).

## Configuration
Edit config/config.py to customize:
SYMBOL: Trading pair (default: "BTCUSDT").

AMOUNT: Trade size in USDT (default: 1).

SENTIMENT_BUY_THRESHOLD: Sentiment sum to buy (default: 0.2).

SENTIMENT_SELL_THRESHOLD: Sentiment sum to sell (default: -0.2).

DCA_THRESHOLD: Price drop percentage for DCA (default: 0.98).




