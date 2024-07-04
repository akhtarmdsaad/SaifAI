from selenium import webdriver
from selenium.webdriver.firefox.options import Options


options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

# Your Selenium Script Here
driver.get('https://google.com')

driver.save_screenshot('sc.png')
driver.quit()
