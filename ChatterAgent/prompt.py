
import json
from jinja2 import BaseLoader, Environment

PROMPT = open("ChatterAgent/prompt.jinja2", "r").read().strip()

class ChatterAgent:
    def __init__(self,llm) -> None:
        self.llm = llm
    
    def render(self,conversations:str,prompt:str,last_response):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversations=conversations,
            user_prompt=prompt
        )
    
    def validate_response(self, response: str):
        response = response.text.strip("`json \n")
        if "response" not in response :
            return False
        else:
            response = json.loads(response)
            return (response["response"])

    def execute(self,prompt,conversations="",last_response=""):
        prompt = self.render(prompt=prompt, conversations=conversations, last_response=last_response)

        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)

        return valid_response