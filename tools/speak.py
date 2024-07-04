import os
from gtts import gTTS
from settings import AUDIO_FILENAME
import time


class Engine:
    def __init__(self) -> None:
        self.engine = gTTS 
    
    def say(self,text):
        start_time = time.time()
        tts = self.engine(text)
        tts.save(AUDIO_FILENAME)

        with open('logs/speak.log','a+') as f:
            f.write('Speak Text:'+text)
            f.write('\nSpeak Generation Time:'+str(time.time()-start_time))
            f.write('\n\n\n')
        
        os.system(f"afplay {AUDIO_FILENAME}")

def validate(text):
    valids = ""
    letters = "abcdefghijklmnopqrstuvwxyz,1234567890 "
    for character in text:
        if character in '.!?$@:;|':
            valids += ','
        elif character in "- ":
            valids += ' '
        elif character.lower() in letters:
            valids += (character)
    return (valids)

def speak(text):
    # engine = Engine()
    # engine.say(text)
    os.system("say "+validate(text))

if __name__ == '__main__':
    speak("Hello Saad, How are you, 1234@34#$")
