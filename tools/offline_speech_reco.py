from vosk import Model, KaldiRecognizer
import json

import pyaudio

# model = Model("/Users/saad/Downloads/vosk-model-small-en-in-0.4")
model = Model("/Users/saad/Downloads/vosk-model-en-us-0.22")

recogniser = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()

stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

def takeCommand():
    stream.start_stream()

    print("Speak")
    started = False
    text_string = ""
    while True:
        data = stream.read(4096, exception_on_overflow = False)
        if not data and started:
            print("nodata")
            continue
        if recogniser.AcceptWaveform(data):
            text = recogniser.Result()
            text = json.loads(text)["text"]
            text_string += text
            if not text and started:
                break 
            elif not started and text:
                started = True
    return text_string
