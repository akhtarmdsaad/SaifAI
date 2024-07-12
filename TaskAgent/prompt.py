
from datetime import datetime
import json
from jinja2 import BaseLoader, Environment
import requests
from TaskAgent.tasks import Tasks
from private import TODOIST_API_KEY

PROMPT = open("TaskAgent/prompt.jinja2", "r").read().strip()

def sorting_key(x):
    x=x[:11].split(" ")
    s="".join(x[0].split(":"))
    n=0#12
    if "p" in x[1]:
        n=120000
    if s[:2] != "12":
        return int(s)+n
    else:
        if "a" in x[1]:
            return int(s)
        return int(s)


def convert_time_to_datetime(time_str):
    # Use strptime to parse the time string
    time_format = "%I:%M:%S %p"  # Format for hours:minutes:seconds AM/PM
    datetime_obj = datetime.strptime(time_str, time_format)
    return datetime_obj


def get_current_key(l):
    now=datetime.now()
    time_format = "%I:%M:%S %p"
    now=convert_time_to_datetime(now.strftime(time_format))
    #s=f"{now.hour}{now.minute}{now.hour}"
    for time in l:
        start,end=time.split(" to ")
        start=convert_time_to_datetime(start)
        end=convert_time_to_datetime(end)
        if now >= start and now < end:
            return time
    return time


class TaskAgent:
    def __init__(self,llm) -> None:
        self.llm = llm
        self.task_agent = Tasks(TODOIST_API_KEY)

        # copy routine from ~/bin/routine.json
        url = "https://routine-4f824-default-rtdb.asia-southeast1.firebasedatabase.app/routine.json"
        self.routine = json.loads(requests.get(url).text)

        # filter json into dict 

        self.keys=list(self.routine.keys())
        self.keys.sort(key=lambda x: sorting_key(x))

        sorted_dict = {i: self.routine[i] for i in self.keys}
        self.routine = sorted_dict



    def get_tasks(self):
        # return only titles 
        tasks = self.task_agent.get_tasks()
        return [task["title"] for task in tasks]
    
    
    def render(self,conversations:str,prompt:str,last_response):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            conversations=conversations,
            user_prompt=prompt,
            list_of_tasks=self.get_tasks(),
            routine=self.routine,
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