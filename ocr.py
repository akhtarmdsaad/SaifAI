import cv2
import pytesseract
from settings import SCREENSHOT_FILENAME 
import logging
from tools.take_screenshot import take_screenshot

logging.basicConfig(filename='app.log.txt', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s')

def get_text_from_image(image_path):
    # Load image
    img = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply threshold to convert to binary image
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Pass the image through pytesseract
    text = pytesseract.image_to_string(threshold_img)
    logging.info("Text from the Screenshot is: "+text)
    # Print the extracted text
    return text 

def get_text_from_screen():
    # Capture the screen
    take_screenshot()
    return get_text_from_image(SCREENSHOT_FILENAME)

    

if __name__ == '__main__':
    print(get_text_from_image("testocr.png"))