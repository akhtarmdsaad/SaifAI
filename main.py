import logging

# Configure logging (assuming logs folder exists)
logging.basicConfig(filename='assistant.log', level=logging.DEBUG)


# Agents
from HelperAgent.prompt import HelperAgent
from NoteTakerAgent.prompt import NoteTakerAgent
from DirectionAgent.prompt import DirectionAgent
from ChatterAgent.prompt import ChatterAgent
from BrowserAgent.prompt import BrowserAgent
from TaskAgent.prompt import TaskAgent
from RealtimeAgent.prompt import RealtimeAgent

from tools.md2text import markdown_to_text
from tools.speech_reco import takeCommand, takeVoskCommand
from tools.speak import speak
from tools.take_screenshot import take_screenshot
import PIL.Image
from settings import SCREENSHOT_FILENAME
from ocr import get_text_from_screen
from llm import LLM

agent = DirectionAgent(LLM())

conversations = ""
last_response = ""


# changing its order also affects the below implementation of code.
agents_dict = {
    "chatter": ChatterAgent(LLM()),
    "screen-reader": HelperAgent(LLM()),
    "note-taker": NoteTakerAgent(LLM()),
    "task-agent": TaskAgent(LLM()),
    "realtime-agent": RealtimeAgent(LLM()),
    # "browser-agent": BrowserAgent(LLM()),
    "exit-agent": None
}

assert sorted(agent.agents_list) == sorted(agents_dict), "All agents present in direction agent should match in main too"


speak("Ready, Please tell your query")
agents_list = list(agents_dict)
exit_conversation = False
while True:
    user_prompt = takeCommand()
    if not user_prompt:
        continue
    print(user_prompt)
    speak("hmm", open_subprocess=True)

    try:
        # get the agent name to run
        agent_name, response, agent_prompt = agent.execute(user_prompt, conversation=conversations)

        print("response forwarded to " + agent_name)
        print("prompt given to agent:", agent_prompt)

        if agent_name != "chatter" and agent_name != "exit-agent":
            print(agent_name)
            response = agents_dict[agent_name].execute(conversations=conversations, last_response=last_response, prompt=agent_prompt)
    except Exception as e:
        logging.error(f"Error during agent execution: {e}")
        speak("Sorry, I encountered an error. Please try again.")
        continue

    if not response:
        continue

    reply = "No reply"
    if agent_name == "chatter":
        reply = response
    elif agent_name == "screen-reader":
        reply = (response[0])
    elif agent_name == "note-taker":
        reply = (response[0])
    elif agent_name == "task-agent":
        reply = (response[0])
    elif agent_name == "realtime-agent":
        reply = (response)
    elif agent_name == "browser-agent":
        reply = (response[0])
    elif agent_name == "exit-agent": 
        exit_conversation = True
        reply = response

    conversations += f"""
User: {user_prompt}
You: {reply}
"""
    speak(markdown_to_text(reply))
    last_response = reply
    print(response)

    if exit_conversation:
        break
