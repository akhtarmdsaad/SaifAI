import requests
from private import NEWS_API_KEY

class News:
    def __init__(self) -> None:
        self.url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&sortBy=popularity"

    def get(self):
        return requests.get(self.url).json()
    
    def get_top_5_articles(self):
        return self.get()["articles"][:5]
    
    def structured_string_to_speak(self):
        data = self.get_top_5_articles()
        string = "Here are the top 5 articles of the day:\n"
        for article in data:
            string += f"{article['title']}\n"
        return string

