import logging
from bs4 import BeautifulSoup
from markdown import markdown
import re

logging.basicConfig(filename='markdown_to_text.log', filemode='a+', format='%(asctime)s - %(levelname)s - %(message)s')

def markdown_to_text(markdown_string):
    """Converts a markdown string to plaintext, handling potential errors.

    Args:
        markdown_string (str): The markdown string to convert.

    Returns:
        str: The extracted plain text, or an empty string if errors occur.
    """

    try:
        # Convert markdown to HTML
        html = markdown(markdown_string)

        # Remove code snippets
        html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
        html = re.sub(r'<code>(.*?)</code >', ' ', html)

        # Parse HTML with BeautifulSoup, handling potential parsing errors
        try:
            soup = BeautifulSoup(html, "html.parser")
            text = ''.join(soup.findAll(string=True))
            return text
        except (AttributeError, TypeError) as e:
            logging.error(f"Error parsing HTML: {e}")
            return ""

    except Exception as e:
        logging.error(f"Unexpected error during markdown conversion: {e}")
        return ""


# Configure logging (optional, adjust as needed)
if __name__ == "__main__":
    # Example usage
    markdown_text = """
    This is a markdown string with some text.

    Here's some code:

    ```python
    print("Hello, world!")
    ```
    """

    print(markdown_to_text(markdown_text))