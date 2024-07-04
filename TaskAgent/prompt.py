
import json
from jinja2 import BaseLoader, Environment
from TaskAgent.tasks import Tasks
from private import TODOIST_API_KEY

PROMPT = open("TaskAgent/prompt.jinja2", "r").read().strip()

class TaskAgent:
    def __init__(self,llm) -> None:
        self.llm = llm
        self.task_agent = Tasks(TODOIST_API_KEY)
    
    
    def render(self,conversations:str,prompt:str,last_response):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversations=conversations,
            user_prompt=prompt,
            list_of_tasks=self.task_agent.get_tasks(),
        )
    
    def validate_response(self, response: str):
        response = response.text.strip("`json \n")
        if "response" not in response or "command" not in response or "task_title" not in response:
            return False
        else:
            response = json.loads(response)

            # clean the command 
            command = response["command"].strip("1234567890. -\n").upper()
            response["command"] = command

            # clean the task_title 
            task_title = response["task_title"].strip()
            response["task_title"] = task_title

            # validate command 
            if response["command"] not in ["ADD","DELETE","NONE","LIST"]:
                return False

            return (response["response"],response["command"],response["task_title"])

    def execute(self,prompt,conversations="",last_response=""):
        prompt = self.render(prompt=prompt, conversations=conversations, last_response=last_response)

        response = self.llm.inference(prompt)
        
        valid_response = self.validate_response(response)

        if valid_response:
            response,command,task_title = valid_response
            
            if command == "ADD":
                self.task_agent.add_task(task_title, 1)
            elif command == "DELETE":
                self.task_agent.delete_task(task_title)
            elif command == "NONE":
                pass
            elif command == "LIST":
                pass

        return (response, command, task_title)