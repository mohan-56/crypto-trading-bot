
import requests
from textblob import TextBlob
from config.config import NEWS_API_KEY,SYMBOL

class SentimentAnalyzer:
    def __init__(self):
        self.url = f"https://newsapi.org/v2/everything?q={SYMBOL}&apiKey={NEWS_API_KEY}"
    
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
                 print(text)
                 if text:
                    analysis = TextBlob(text)
                    sentiment_score += analysis.sentiment.polarity
                    count += 1
            print("sentiment score",sentiment_score," cnt:",count)
            return sentiment_score / count if count > 0 else 0
        except Exception as e:
            print(f"Error fetching news: {e}")
            return 0




