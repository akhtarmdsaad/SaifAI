
# Agents
from HelperAgent.prompt import HelperAgent
from NoteTakerAgent.prompt import NoteTakerAgent
from DirectionAgent.prompt import DirectionAgent
from ChatterAgent.prompt import ChatterAgent
from TaskAgent.prompt import TaskAgent
from RealtimeAgent.prompt import RealtimeAgent

from tools.md2text import markdown_to_text
# from tools.speech_reco import takeCommand
from tools.offline_speech_reco import takeCommand
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
    "screen-helper":HelperAgent(LLM()),
    "note-taker":NoteTakerAgent(LLM()),
    "task-agent":TaskAgent(LLM()),
    "realtime-agent":RealtimeAgent(LLM())
}

assert sorted(agent.agents_list) == sorted(agents_dict), "All agents present in direction agent should match in main too"

speak("Ready, Please tell your query")
while True:
    user_prompt = takeCommand()
    if not user_prompt:
        continue

    
    agent_name = agent.execute(user_prompt, conversation=conversations)
    # speak("response forwarded to " + agent_name)
    print("response forwarded to " + agent_name)
    response = agents_dict[agent_name].execute(conversations=conversations, last_response=last_response, prompt=user_prompt)
    
    if not response:
        continue

    agents_list = list(agents_dict)    
    reply = "No reply"
    if agent_name == agents_list[0]:
        reply = response
    elif agent_name == agents_list[1]:
        reply = (response[0])
    elif agent_name == agents_list[2]:
        reply = (response[0])
    elif agent_name == agents_list[3]:
        reply = (response[0])
    elif agent_name == agents_list[4]:
        reply = (response)
    
    conversations += f"""
User: {user_prompt}
You: {reply}
"""
    speak(markdown_to_text(reply))
    last_response = reply
    print(response)
