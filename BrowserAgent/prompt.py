import os
from jinja2 import BaseLoader, Environment
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from settings import BROWSER_SCREEN, DOWNLOADS_DIR
import time
import json
import re

from tools.speak import speak

PROMPT = open("BrowserAgent/prompt.jinja2", "r").read().strip()
class BrowserAgent:
    def __init__(self, llm):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.llm = llm
        self.extracted_data = ""
        self.downloaded_files = []
        self.current_error = ""

    def navigate(self, url):
        self.driver.get(url)

    def get_page_source(self):
        return self.driver.page_source

    def get_filtered_page_source(self):
        soup = BeautifulSoup(self.get_page_source(), 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        
        # return in html form
        return str(soup)

    def get_screenshot(self):
        self.driver.save_screenshot(BROWSER_SCREEN)

    def fill_form(self, form_data):
        for field, value in form_data.items():
            element = self.driver.find_element(By.NAME, field)
            element.send_keys(value)
    
    def submit_form(self, submit_button_selector):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, submit_button_selector)
        submit_button.click()
    
    def click_button(self, selector):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            element.click()
        except Exception as e:
            return str(e)

    def scroll_to_element(self, selector):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        except Exception as e:
            return str(e)

    def take_screenshot(self, filename):
        try:
            self.driver.save_screenshot(filename)
        except Exception as e:
            return str(e)

    def check_element(self, selector):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except TimeoutException:
            return False
        except Exception as e:
            return False

    def execute_script(self, script):
        try:
            return self.driver.execute_script(script)
        except Exception as e:
            return str(e)

    def llm_process(self, prompt, image=False):
        return self.llm.inference(prompt, explicit_image=image)
    
    def to_json(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"status":"invalid JSON format, rejected by software"}

    def execute_task(self, task_description):
        result = None
        self.extracted_data = ""
        previous_response = ""
        current_error = ""
        max_attempts = 5
        attempt = 0

        while result is None and attempt < max_attempts:
            attempt += 1
            plan_prompt = self.generate_plan_prompt(task_description, previous_response, current_error + "\n" + self.current_error)
            
            print("Asking LLM for a plan")
            execution_plan = self.get_execution_plan(plan_prompt, current_error or self.current_error)
            
            if not execution_plan:
                continue
            self.current_error = ""
            current_error = ""
            print("Plan generated, now executing")
            try:
                speak(execution_plan['response'], open_subprocess=True)
                result = self.execute_plan(execution_plan)
                if result:
                    break
                attempt = 0
            except Exception as e:
                print(f"Error executing plan: {e}")
                current_error = str(e)
            
            previous_response += f"\n{json.dumps(execution_plan)}"

        if result:
            return result
        else:
            return f"Failed to complete task after {max_attempts} attempts"

    def render_prompt(self, task_description, previous_response, current_error):
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            task_description=task_description, 
            filtered_page_source=self.get_filtered_page_source(), 
            extracted_data=self.extracted_data, 
            previous_response=previous_response, 
            current_error=current_error,
            downloaded_files=self.downloaded_files
        )

    def generate_plan_prompt(self, task_description, previous_response, current_error):
        prompt = self.render_prompt(task_description=task_description, previous_response=previous_response, current_error=current_error)
        return prompt

    def get_execution_plan(self, plan_prompt, is_error):
        self.get_screenshot()
        execution_plan = self.llm_process(plan_prompt, image=BROWSER_SCREEN)
        
        
        return self.validate_response(execution_plan)

    def execute_plan(self, plan):
        if plan['status'] == 'completed':
            return plan['result']
        
        for step in plan['next_steps']:
            action = step['action']
            params = step['parameters']
            
            if action == 'navigate':
                self.navigate(params['url'])
            elif action == 'fill_form':
                self.fill_form(params['form_data'])
            elif action == 'extract':
                self.extracted_data = self.extract_data(params['selector'])
            elif action == 'submit_form':
                self.submit_form(params['submit_button_selector'])
            elif action == 'wait':
                time.sleep(params['seconds'])
            elif action == 'download':
                self.download_file(params['url'], params['filename'])
            elif action == 'click_button':
                self.click_button(params['selector'])
            elif action == 'scroll_to_element':
                self.scroll_to_element(params['selector'])
            elif action == 'check_element':
                self.check_element(params['selector'])
            elif action == 'execute_script':
                self.execute_script(params['script'])
            else:
                raise ValueError(f"Unknown action: {action}")
        
        return None
    
    def validate_response(self, response: str):
        response = response.text.strip("`json \n")
        response = self.to_json(response)
        if "response" not in response or "status" not in response or "result" not in response or "next_steps" not in response:
            return False
        else:
            return response

    def extract_data(self, selector):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            text = element.text
            url = element.get_attribute('href')
            return {
                'text': text,
                'url': url
            }
        except Exception as e:
            print(f"Error extracting data: {e}")
            return {
                'text': "",
                'url': ""
            }
        
    def download_file(self, url, filename):
        try:
            response = requests.get(url)
            filename = os.path.join(DOWNLOADS_DIR, filename)
            if not os.path.exists(DOWNLOADS_DIR):
                os.makedirs(DOWNLOADS_DIR)
            if os.path.exists(filename):
                n=1
                while os.path.exists(filename):
                    filename = os.path.join(DOWNLOADS_DIR, f"{n}_{filename}")
                    n+=1
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Successfully downloaded: {filename}")
                self.downloaded_files.append(f"file: {filename}, url: {url}\n")
                return f"Successfully downloaded: {filename}"
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
                self.current_error += f"Failed to download {url}. Status code: {response.status_code}\n"
        except Exception as e:
            print(f"Error downloading file: {e}")
            self.current_error += f"Error downloading file: {e}\n"

    def execute(self, conversations, prompt, last_response):
        return self.execute_task(prompt)

    def close(self):
        self.driver.quit()

