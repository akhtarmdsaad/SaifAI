import pyscreenshot
from settings import SCREENSHOT_FILENAME

def take_screenshot():
    image = pyscreenshot.grab() 
    image.save(SCREENSHOT_FILENAME)
    
