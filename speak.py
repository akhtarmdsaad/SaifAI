import os
import pyttsx3
engine = pyttsx3.init()

def validate(text):
    valids = ""
    letters = "abcdefghijklmnopqrstuvwxyz"
    for character in text:
        if character.lower() in letters:
            valids += (character)
    return (valids)

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    speak("Hello Saad, How are you")
