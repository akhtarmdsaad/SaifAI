
import json
from jinja2 import BaseLoader, Environment
from RealtimeAgent.weather import Weather
from RealtimeAgent.news import News

PROMPT = open("RealtimeAgent/prompt.jinja2", "r").read().strip()

class RealtimeAgent:
    def __init__(self,llm) -> None:
        self.llm = llm
    
    def tell_current_time_and_date(self):
        from datetime import datetime
        now = datetime.now()
        return f"Current time is {now.strftime('%H:%M:%S')} and today is {now.strftime('%d-%m-%Y')}"
    
    def current_weather_data(self,city=None):
        """
        if no city name provided, it gives your city data
        """
        if city:
            return Weather().search(city)
        else:
            return Weather().search()
    
    def get_news(self):
        return News().structured_string_to_speak()
    
    def render(self,conversations:str,prompt:str,last_response):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversations=conversations,
            user_prompt=prompt,
            current_time=self.tell_current_time_and_date(),
            weather_data=self.current_weather_data()
        )
    
    def validate_response(self, response: str):
        response = response.text.strip("`json \n")
        if "response" not in response or "command" not in response:
            return False
        else:
            response = json.loads(response)

            if response["response"] == "" or response["command"] == "" or not response["command"].isdigit():
                return False

            return (response["response"], response["command"])

    def execute(self,prompt,conversations="",last_response=""):
        prompt = self.render(prompt=prompt, conversations=conversations, last_response=last_response)

        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)

        # commands
        # 1. tell current time and date
        # 2. tell current weather   
        # 3. tell current news
        response = "I'm sorry, I don't understand"
        if valid_response:
            response, command = valid_response
            if command == "3":
                response = self.get_news()
        else:
            print("response is not valid")
            print(valid_response)

        return response