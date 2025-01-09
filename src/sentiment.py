
import requests
from textblob import TextBlob
from config.config import NEWS_API_KEY

class SentimentAnalyzer:
    def __init__(self):
        self.url = f"https://newsapi.org/v2/everything?q=cryptocurrency&apiKey={NEWS_API_KEY}"
    
    def get_sentiment(self):
        try:
            response = requests.get(self.url)
            news_data = response.json()
            articles = news_data.get("articles", [])
            print(response)
            sentiment_score = 0
            count = 0
            for article in articles[:10]:  # Top 10 articles
                # text = article["title"] + " " + article["description"]
                 title = article.get("title", "")
                 description = article.get("description", "") or ""
                 text = f"{title} {description}".strip()
                 if text:
                    analysis = TextBlob(text)
                    sentiment_score += analysis.sentiment.polarity
                    count += 1
            print("sentiment score",sentiment_score)
            return sentiment_score / count if count > 0 else 0
        except Exception as e:
            print(f"Error fetching news: {e}")
            return 0





# import requests
# from textblob import TextBlob

# class SentimentAnalyzer:
#     def __init__(self):
#         self.url = "https://api.coingecko.com/api/v3/news"  # CoinGecko news endpoint
    
#     def get_sentiment(self):
#         try:
#             response = requests.get(self.url)
#             response.raise_for_status()  # Raise an error for bad status codes
#             news_data = response.json()
#             articles = news_data.get("data", [])  # CoinGecko returns news in "data" key
            
#             sentiment_score = 0
#             count = 0
#             for article in articles[:10]:  # Analyze top 10 articles
#                 title = article.get("title", "")
#                 description = article.get("description", "") or ""
#                 text = f"{title} {description}".strip()
#                 if text:  # Ensure there's text to analyze
#                     analysis = TextBlob(text)
#                     sentiment_score += analysis.sentiment.polarity  # -1 (negative) to 1 (positive)
#                     count += 1
            
#             return sentiment_score / count if count > 0 else 0
#         except requests.RequestException as e:
#             print(f"Error fetching news from CoinGecko: {e}")
#             return 0
#         except Exception as e:
#             print(f"Error processing sentiment: {e}")
#             return 0