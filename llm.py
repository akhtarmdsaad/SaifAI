import logging
import time
import PIL.Image
import google.generativeai as genai
import private
import random
from datetime import datetime
from settings import SCREENSHOT_FILENAME
from tools.take_screenshot import take_screenshot
genai.configure(api_key=random.choice(private.GEMINI_API_KEY))


filename = f"llm_logs/llm_log_({datetime.astimezone(datetime.now())}).log"

class LLM:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    def inference(self, prompt, *args, image=False, explicit_image=False):
        # takes in prompt and returns response from llm 
        start_time = time.time()
        try:
            if image:
                take_screenshot()
                image = PIL.Image.open(SCREENSHOT_FILENAME)
                response = self.model.generate_content([prompt, image, *args])
            elif explicit_image:
                explicit_image = PIL.Image.open(explicit_image)
                response = self.model.generate_content([prompt, explicit_image, *args])
            else:
                response = self.model.generate_content([prompt, *args])
        except Exception as e:
            logging.error(f"Error during LLM call: {e}")
            return "An error occurred while processing your request."
        
        self.log(prompt,response,time.time()-start_time)
        
        # Handle potential errors in response generation (unchanged)
        if not response.text:
            logging.error("Error: Empty response from LLM")
            return "An error occurred while processing your request."

        
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