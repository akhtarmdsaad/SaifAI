import time
from vosk import Model, KaldiRecognizer
import json

import pyaudio

model = Model("/Users/saad/Downloads/vosk-model-small-en-in-0.4")
# model = Model("/Users/saad/Downloads/vosk-model-en-us-0.22")

recogniser = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
def takeCommand():

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

    stream.start_stream()

    print("Speak")
    started = False
    text_string = ""
    while True:
        data = stream.read(1024, exception_on_overflow = False)
        
        if recogniser.AcceptWaveform(data):
            print("Analysing...")
            starttime = time.time()
            text = recogniser.Result()
            print("Analysed. time:",time.time()-starttime)
            text = json.loads(text)["text"]
            text_string += text + " "
            print(text, end=" ")
            if not text and started:
                break 
            elif not started and text:
                started = True
    print()
    stream.close()
    return text_string
if __name__ == "__main__":
    text = takeCommand()
    print("You spoke:",text)
    print()