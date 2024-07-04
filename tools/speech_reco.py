import time
import speech_recognition as sr 

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

def takeVoskCommand():
    pass

if __name__ == "__main__":
    takeVoskCommand()