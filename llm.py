
# This is the main llm file which sends the request and gets the response

import google.generativeai as genai
import PIL.Image
import private
from settings import SCREENSHOT_FILENAME

genai.configure(api_key=private.GEMINI_API_KEY)
# img = PIL.Image.open(SCREENSHOT_FILENAME)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
filename = "llm_log.log"

class LLM:
    def __init__(self) -> None:
        pass

    def inference(self,prompt, *args):
        # takes in prompt and returns response from llm 
        response = model.generate_content([prompt, *args])

        # log the data 
        with open(filename,"a+") as f:
            f.write("\nPrompt: " + prompt+"\n")
            f.write("\nResponse: "+response.text+"\n\n")

        return response    

        
def make_prompt(prompt,img=False):
    f = open(filename,"a+")
    f.write("\nPrompt: " + prompt+"\n")

    if img:
        # if user want to send image, then the screenshot will get sent
        # be aware that img in't getting sent, but the screenshot is sent
        response = model.generate_content([prompt, PIL.Image.open(SCREENSHOT_FILENAME)])
    else:
        # this is for simple text based prompt 
        response = model.generate_content(prompt)
    text = response.text.strip("`json")
    f.write("\nResponse: "+text+"\n\n")
    f.close()
    return text