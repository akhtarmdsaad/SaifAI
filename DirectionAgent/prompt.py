

import json
from jinja2 import BaseLoader, Environment

PROMPT = open("DirectionAgent/prompt.jinja2", "r").read().strip()

class DirectionAgent:
    def __init__(self,llm) -> None:
        self.llm = llm
        self.agents_list = {
            "screen-helper": "Reads the Screentext and helps the user answer thier questions. Provides the context and text based response.",
            "chatter": "Reply to the users prompt. Provides text based response",
            "note-taker": "Gets the context, create files and write important notes in there.",
            "task-agent": "Helps the user manage their tasks. Add, delete, and list the tasks.",
            "realtime-agent": "Provides the real time information like time, weather, news etc.",
        }
    
    def render(self,prompt, conversation):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            user_prompt=prompt,
            conversation=conversation,
            agents_list=self.agents_list
        )
    
    def validate_response(self, response: str):
        response = response.text.strip("`json \n")
        if "agent_name" not in response :
            return False
        else:
            response = json.loads(response)
            if response["agent_name"] not in self.agents_list:
                return False
            return (response["agent_name"])

    def execute(self,prompt,conversation):
        prompt = self.render(prompt, conversation)

        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)

        return valid_response

