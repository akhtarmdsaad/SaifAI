import cv2
import pytesseract
from settings import SCREENSHOT_FILENAME
import logging
from tools.take_screenshot import take_screenshot

# Configure detailed logging for better debugging and analysis
logging.basicConfig(
    filename='app.log.txt',
    filemode='a+',
    format='%(asctime)s - %(levelname)s - %(message)s - %(funcName)s:%(lineno)d',
    level=logging.DEBUG  # Enable more detailed logs
)


def get_text_from_image(image_path):
    """Extracts text from an image, handling potential errors gracefully.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Extracted text, or an empty string if errors occur.
    """

    try:
        # Load image with error handling
        img = cv2.imread(image_path)
        if img is None:
            logging.error(f"Error loading image: {image_path}")
            return ""

        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply threshold to convert to binary image with informative message
        threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        logging.info(f"Converted image to binary: {image_path}")

        # Pass the image through pytesseract with specific exception handling
        try:
            text = pytesseract.image_to_string(threshold_img)
            logging.info(f"Text extracted from image: {text}")
            return text
        except pytesseract.pytesseract.TesseractError as e:
            logging.error(f"Error extracting text with Tesseract: {e}")
            return ""

    except Exception as e:
        logging.critical(f"Unexpected error during image processing: {e}")
        return ""


def get_text_from_screen():
    """Captures a screenshot and extracts text, handling errors.

    Returns:
        str: Extracted text, or an empty string if errors occur.
    """

    try:
        # Capture the screen
        take_screenshot()
        return get_text_from_image(SCREENSHOT_FILENAME)

    except Exception as e:
        logging.critical(f"Error capturing screenshot or processing image: {e}")
        return ""


if __name__ == '__main__':
    extracted_text = get_text_from_image("testocr.png")
    if extracted_text:
        print(extracted_text)
    else:
        print("Failed to extract text. Please check the logs (app.log.txt) for details.")
