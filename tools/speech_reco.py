import json
import time
import pyaudio
import speech_recognition as sr

from tools.speak import speak 



def takeCommand():
    
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")    
        start_time = time.time()
        query = r.recognize_google(audio, language ='en-in')
        
        with open('logs/speech_reco.log','a+') as f:
            f.write('Speech Text:'+query)
            f.write('\nSpeech Recognition Time:'+str(time.time()-start_time))
            f.write('\n\n\n')
        print(f"User said: {query}\n")

  
    except Exception as e:
        print(e)    
        print("Unable to Recognize your voice.")  
        return ""
     
    return query

def takeVoskCommandOld():
    from vosk import Model, KaldiRecognizer
    r = sr.Recognizer()
    model = Model("/Users/saad/Downloads/vosk-model-small-en-in-0.4")
    # model = Model("/Users/saad/Downloads/vosk-model-en-us-0.22")

    recogniser = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()

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

def takeVoskCommand1():
    from vosk import Model, KaldiRecognizer
    import speech_recognition as sr
    import pyaudio
    
    r = sr.Recognizer()
    model = Model("/Users/saad/Downloads/vosk-model-small-en-in-0.4")
    # model = Model("/Users/saad/Downloads/vosk-model-en-us-0.22")
    recogniser = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Speak")
    started = False
    text_string = ""
    
    while True:
        data = stream.read(4096)
        if recogniser.AcceptWaveform(data):
            result = recogniser.Result()
            text = result[14:-3]  # Extract the recognized text from the JSON result
            if len(text) > 0:
                if not started:
                    print("Started listening...")
                    started = True
                text_string += text + " "
            else:
                if started:
                    print("Stopped listening.")
                    break
    
    stream.stop_stream()
    stream.close()
    mic.terminate()
    
    return text_string.strip()

import time
from vosk import Model, KaldiRecognizer
import pyaudio

# model = Model("/Users/saad/Downloads/vosk-model-small-en-in-0.4")
# model = Model("/Users/saad/Downloads/vosk-model-en-us-0.22")
model = Model("/Users/saad/Downloads/vosk-model-en-in-0.5")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

def takeVoskCommand():
    text_string = ""
    last_speech_time = time.time()
    silence_threshold = 5  # seconds of silence to stop listening
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print("Text:", result)
            text = result[14:-3]  # Extract the recognized text from the JSON result
            if text:
                print(f"Recognized: {text}")
                text_string += text + " "
                last_speech_time = time.time()
        else:
            if time.time() - last_speech_time > silence_threshold:
                print("Stopped listening due to silence.")
                break
    
    return text_string.strip()


if __name__ == "__main__":
    text = ""
    while not text:
        text = (takeVoskCommand())
    print(text)
    
    stream.stop_stream()
    stream.close()
    mic.terminate()