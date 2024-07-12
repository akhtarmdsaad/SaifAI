import os
import subprocess
from gtts import gTTS
from settings import AUDIO_FILENAME
import time
import logging

logging.basicConfig(filename="tts.log", filemode="a+", format="%(asctime)s - %(levelname)s - %(message)s")

class Engine:
    def __init__(self) -> None:
        self.engine = gTTS  # Initialize gTTS engine

    def say(self, text):
        """
        Converts text to speech and saves it to an audio file.

        Args:
            text (str): The text to be spoken.

        Returns:
            None
        """

        start_time = time.time()
        try:
            tts = self.engine(text)
            tts.save(AUDIO_FILENAME)
            logging.info(f"Text converted to speech and saved to {AUDIO_FILENAME}")
        except Exception as e:
            logging.error(f"Error during text-to-speech conversion: {e}")
            return

        try:
            with open("logs/speak.log", "a+") as f:
                f.write(f"Speak Text: {text}\n")
                f.write(f"Speak Generation Time: {time.time() - start_time}\n\n\n")
            logging.info("Speech generation time logged successfully.")
        except Exception as e:
            logging.error(f"Error writing to speak.log: {e}")

        os.system(f"afplay {AUDIO_FILENAME}")


def validate(text):
    """
    Validates the given text for compatibility with the 'say' command.

    Args:
        text (str): The text to be validated.

    Returns:
        str: The validated text.
    """

    valids = ""
    letters = "abcdefghijklmnopqrstuvwxyz,1234567890 "
    for character in text:
        if character in ".!?$@:;|":
            valids += ","
        elif character in "- ":
            valids += " "
        elif character.lower() in letters:
            valids += character
    return valids


def speak(text, open_subprocess=False):
    """
    Speaks the given text using either the gTTS engine or the system 'say' command.

    Args:
        text (str): The text to be spoken.
        open_subprocess (bool, optional): If True, uses 'say' command in a separate process. Defaults to False.
    """

    if open_subprocess:
        # Use a separate process for system 'say' command
        try:
            subprocess.Popen(["say", validate(text)])
            logging.info("Text spoken using system 'say' command in a separate process.")
        except Exception as e:
            logging.error(f"Error using 'say' command: {e}")
    else:
        # Use gTTS engine (assuming initialized)
        os.system("say " + validate(text))

def speak(text,*args,**kwargs):
    """
    Speaks the given text using the gTTS engine.

    Args:
        text (str): The text to be spoken.
    """

    try:
        engine = Engine()
        engine.say(text)
        logging.info("Text spoken using gTTS engine.")
    except Exception as e:
        logging.error(f"Error using gTTS engine: {e}")

if __name__ == "__main__":
    
    speak("Hello Saad, How are you, 1234@34#$")
