import requests
from private import NEWS_API_KEY

class News:
    def __init__(self) -> None:
        if not NEWS_API_KEY:
            self.url = ""
        self.url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&sortBy=popularity"

    def get(self):
        if not self.url:
            return {"status": "News API key is not provided"}
        return requests.get(self.url).json()
    
    def get_articles(self):
        if not self.url:
            return []
        return self.get()["articles"]
    
    def get_top_5_articles(self):
        if not self.url:
            return []
        articles = self.get_articles()
        return articles[:5]
    
    def structured_string_to_speak(self):
        data = self.get_articles()
        string = ""
        for article in data:
            string += f"{article['title']}\n"
        return string

