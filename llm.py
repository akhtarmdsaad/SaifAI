
# This is the main llm file which sends the request and gets the response

import time
import PIL.Image
import google.generativeai as genai
import private
from datetime import datetime
from settings import SCREENSHOT_FILENAME
from tools.take_screenshot import take_screenshot
genai.configure(api_key=private.GEMINI_API_KEY)


filename = f"llm_logs/llm_log_({datetime.astimezone(datetime.now())}).log"

class LLM:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def inference(self,prompt, *args,image=False,explicit_image=False):
        # takes in prompt and returns response from llm 
        start_time = time.time()
        if image:
            take_screenshot()
            image = PIL.Image.open(SCREENSHOT_FILENAME)
            response = self.model.generate_content([prompt,image, *args])
        elif explicit_image:
            explicit_image = PIL.Image.open(explicit_image)
            response = self.model.generate_content([prompt,explicit_image, *args])
        else:
            response = self.model.generate_content([prompt, *args])
        
        self.log(prompt,response,time.time()-start_time)
        
        return response


    def log(self,prompt,response,time=None):
        # log the data 
        with open(filename,"a+") as f:
            f.write("\nPrompt: " + prompt+"\n")
            try:
                f.write("\nResponse: "+response.text+"\n\n")
            except Exception as e:
                f.write("\nResponse Error: "+str(response)+"\n\n")
            if time:
                f.write("Time taken for above response: "+str(round(time,2))+" seconds")

        return True

        
# def make_prompt(prompt,img=False):
#     f = open(filename,"a+")
#     f.write("\nPrompt: " + prompt+"\n")

#     if img:
#         # if user want to send image, then the screenshot will get sent
#         # be aware that img in't getting sent, but the screenshot is sent
#         response = model.generate_content([prompt, PIL.Image.open(SCREENSHOT_FILENAME)])
#     else:
#         # this is for simple text based prompt 
#         response = model.generate_content(prompt)
#     text = response.text.strip("`json")
#     f.write("\nResponse: "+text+"\n\n")
#     f.close()
#     return text