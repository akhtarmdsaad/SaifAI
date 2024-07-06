

import json
from jinja2 import BaseLoader, Environment

PROMPT = open("DirectionAgent/prompt.jinja2", "r").read().strip()

class DirectionAgent:
    def __init__(self,llm) -> None:
        self.llm = llm
        self.agents_list = {
            "screen-reader": "Reads the Screentext and helps the user answer thier questions. Provides the context and text based response.",
            "chatter": "Reply to the users prompt. Provides text based response. the response is given by gemini llm",
            "note-taker": "Gets the context, create files and write important notes in there.",
            "task-agent": "Helps the user manage their tasks. Add, delete, and list the tasks.\nIt also have the user's routine that tells what the user is supposed to do now.",
            "realtime-agent": "Provides the real time information like time, weather, news etc.",
            "browser-agent": "Helps the user to search the web and get the information from the web.\nNOTE:This agent takes long time to get the information. Choose this agent wisely."
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
        response = json.loads(response)
        if "agent_name" not in response or "response" not in response and "prompt" not in response:
            return False
        else:
            if response["agent_name"] not in self.agents_list:
                return False
            return (response["agent_name"],response["response"], response["prompt"])

    def execute(self,prompt,conversation):
        prompt = self.render(prompt, conversation)

        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)

        return valid_response

