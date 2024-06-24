import json
from jinja2 import Environment, BaseLoader
import llm


PROMPT = open("prompt.jinja2", "r").read().strip()

class HelperAgent:
    def __init__(self) -> None:
        self.name = "Saif Helper"
    
    def render_text(self, conversation:str, last_response:str, screentext:str) -> str :
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversation=conversation,
            last_response=last_response,
            screentext=screentext
        )
    
    def render_image(self, conversation:str, last_response:str) -> str :
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversation=conversation,
            last_response=last_response,
            screentext="Screen Image is provided"
        )


    def validate_response(self, response: str):
        if "response" not in response and "context" not in response and "filtered_screentext" not in response:
            return False
        else:
            print(response)
            response = json.loads(response)
            return (response["response"], response["context"], response["filtered_screentext"])
    
    def execute(self, conversation: list, last_response:str, screentext:str = "", image=False ) -> str:
        if image:
            prompt = self.render_image(conversation, last_response)
        else:
            prompt = self.render_text(conversation, last_response, screentext)
        response = llm.make_prompt(prompt,image)
        
        valid_response = self.validate_response(response)
        
        return valid_response