import json
import os
from jinja2 import Environment, BaseLoader
from datetime import datetime


PROMPT = open("NoteTakerAgent/prompt.jinja2", "r").read().strip()
NOTES_FOLDER = "notes/"

class NoteTakerAgent:
    def __init__(self, llm) -> None:
        self.name = "note taker"
        self.llm = llm


    def render(self,prompt, conversation:str, last_response:str) -> str :
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversation=conversation,
            last_response=last_response,
            prompt=prompt
        )


    def validate_response(self, response: str):
        response = response.text.strip("`json \n")
        if "response" not in response and "context" not in response and "notes" not in response:
            return False
        else:
            response = json.loads(response)
            return (response["response"], response["context"], response["notes"])


    def execute(self, conversations: list, last_response:str, prompt:str) -> str:
        prompt = self.render(conversation=conversations, last_response=last_response,prompt=prompt)
        response = self.llm.inference(prompt, image=True)
        


        valid_response = self.validate_response(response)

        now = datetime.now()
        filename = f"notes_{now.day}-{now.month}-{now.year}.{now.hour}-{now.minute}-{now.second}.txt"
        f = open(os.path.join(NOTES_FOLDER,filename),"w+")
        f.write(valid_response[2])
        f.close()

        return valid_response