from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from settings import BROWSER_SCREEN
import bs4 
from llm import LLM
from jinja2 import Environment, BaseLoader

SUMMARISE_PROMPT = open("BrowserAgent/summarize.jinja2", "r").read().strip()

class Browser:
    def __init__(self) -> None:
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.llm = LLM()
    
    def save_screenshot(self):
        self.driver.save_screenshot(BROWSER_SCREEN)
    
    def get_driver(self):
        return self.driver
    
    def quit(self):
        self.driver.quit()

    def __del__(self):
        self.driver.quit()
    
    def google_search(self,query):
        self.driver.get(f"https://www.google.com/search?q={query}")
    
    def open_first_page(self, query):
        """
        search for the query on google and return the page source of the first link
        """
        self.google_search(query)

        # click on the first link
        first_link = self.driver.find_element(By.CSS_SELECTOR, 'h3')
        first_link.click()

        # get the page source of the new page
        page_source = self.driver.get_page_source()
        return page_source
    
    def answer_query(self, query):
        """
        fetches query, learns about it and answers it.
        """
        self.open_first_page(query)
        return self.summarize_webpage(query)
    
    def get_screenshot(self):
        return self.driver.get_screenshot_as_png()

    def get_page_source(self):
        return self.driver.page_source
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_title(self):
        return self.driver.title
    
    def get_cookies(self):
        return self.driver.get_cookies()

    
    def scrape_text_from_source(self):
        soup = bs4.BeautifulSoup(self.get_page_source(),'html.parser')

        # remove scripts and styles 
        for script in soup(["script", "style"]):
            script.extract()
        
        # convert into chunks
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

        # remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text 
    
    def click_on_element(self, css_selector_string):
        element = self.driver.find_element_by_css_selector(css_selector_string)
        element.click()
    
    def fill_form(self, css_selector_string, value):
        element = self.driver.find_element_by_css_selector(css_selector_string)
        element.send_keys(value)
    
    def get_buttons(self):
        return self.driver.find_elements_by_tag_name('button')
    
    def get_links(self):
        return self.driver.find_elements_by_tag_name('a')
    
    def get_form_fields(self):
        return self.driver.find_elements_by_tag_name('input')
    
    def scrape_links_from_source(self):
        soup = bs4.BeautifulSoup(self.get_page_source(),'html.parser')

        # remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        return links
    
    def scrape_images_from_source(self):
        soup = bs4.BeautifulSoup(self.get_page_source(),'html.parser')

        # remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()

        images = []
        for img in soup.find_all('img'):
            images.append(img.get('src'))
        return images
    
    def extract_code_from_github_url(self):
        if 'github.com' in self.get_current_url():
            soup = bs4.BeautifulSoup(self.get_page_source(),'html.parser')
            code = soup.find_all('td',class_='blob-code blob-code-inner')
            return code
        else:
            return None
    
    def render_summary_prompt(self, text, question):
        env = Environment(loader=BaseLoader())
        template = env.from_string(SUMMARISE_PROMPT)
        return template.render(text=text, question=question)

    def summarize_text(self, text, question):
        prompt = self.render_summary_prompt(text=text, question=question)
        response = self.llm.inference(prompt)
        return response
    
    def summarize_webpage(self, question):
        text = self.scrape_text_from_source()
        return self.summarize_text(text, question)
    