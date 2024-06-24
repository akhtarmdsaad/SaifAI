
from prompt import HelperAgent
from speak import speak 
from take_screenshot import take_screenshot
from settings import DO_FROM_IMAGE
from ocrTest import get_text_from_screen

agent = HelperAgent()

conversations = ""
last_response = ""


while True:
    user_prompt = input("Enter the Prompt\n>")
    # Get screen
    
    if DO_FROM_IMAGE:
        take_screenshot()
        response = agent.execute(conversations, last_response,image=DO_FROM_IMAGE)
    else:
        text = get_text_from_screen()
        response = agent.execute(conversations, last_response, screentext=text)
    if not response:
        print("Response validation failed")
    
    
    speak(response[0])
    print(response)
    