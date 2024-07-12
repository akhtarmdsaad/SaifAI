import os
import threading
import subprocess
import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Function to say something using subprocess
def say_something(text):
    process = subprocess.Popen(['say', text])
    return process

# VAD class using Vosk
class VAD:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=pyaudio.paInt16,
                                        channels=1,
                                        rate=16000,
                                        input=True,
                                        frames_per_buffer=4000)
        self.running = True

    def detect(self):
        data = self.stream.read(4000, exception_on_overflow=False)
        if self.rec.AcceptWaveform(data):
            result = json.loads(self.rec.Result())
            if result['text']:
                print("User is speaking...:", result['text'])
                return "speak"
        else:
            partial_result = json.loads(self.rec.PartialResult())
            if partial_result['partial']:
                print("User is starting to speak...")
                return "speak"
            
        return None
            

    def stop(self):
        self.running = False
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio.terminate()

# Function to run VAD in a separate thread
def run_vad(vad_instance, say_process):
    print("Poll:",say_process.poll())
    while say_process.poll() == None and vad_instance.detect() == None:  # Check if process is still running
        pass
    if say_process.poll() == None:
        say_process.terminate()
    print("Poll:",say_process.poll())
    # vad_instance.stop()  # Stop the VAD instance when the say process ends




model_path = "/Users/saad/Downloads/vosk-model-en-in-0.5"  # Path to the Vosk model directory
vad_instance = VAD(model_path)
    
# Main function
def speak(text, open_subprocess=False):
    if open_subprocess == False:
        print("NOTE: This speak function always runs in open subprocess mode")

    say_process = say_something(text)
    
    vad_thread = threading.Thread(target=run_vad, args=(vad_instance, say_process))
    vad_thread.start()

    try:
        vad_thread.join()  # Wait for the VAD thread to complete
    except KeyboardInterrupt:
        vad_instance.stop()
        if say_process.poll() is None:
            say_process.terminate()

if __name__ == "__main__":
    speak("Hello, how are you today?")
