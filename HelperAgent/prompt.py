import json
from jinja2 import Environment, BaseLoader


PROMPT = open("HelperAgent/prompt.jinja2", "r").read().strip()

class HelperAgent:
    def __init__(self, llm) -> None:
        self.name = "Helper"
        self.llm = llm


    def render(self,prompt:str, conversations:str, last_response:str) -> str :
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversations=conversations,
            last_response=last_response,
            user_prompt=prompt
        )


    def validate_response(self, response: str):
        response = response.text.strip("`json")
        if "response" not in response and "context" not in response and "filtered_screentext" not in response:
            return False
        else:
            response = json.loads(response)
            return (response["response"], response["context"], response["filtered_screentext"])


    def execute(self, conversations: list, last_response:str, prompt:str) -> str:
        prompt = self.render(conversations=conversations, last_response=last_response, prompt=prompt)
        response = self.llm.inference(prompt, image=True)
        
        valid_response = self.validate_response(response)

        return valid_response