import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import pyaudio
from datetime import date
import time

# for OpenAI TTS model
from openai import OpenAI
import pygame 
client = OpenAI()

pygame.mixer.init()
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# set the Google Gemini API key as a system environment variable or add it here
# genai.configure(api_key="AIzaSyBb0ql7MJMUNVKGtt3vkVgBd59Ow17Ppxk ")

today = str(date.today())

engine = pyttsx3.init()

engine.setProperty('rate', 190) # speaking rate 
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id) # 0 for male; 1 for female

# model of Google Gemini API
model = genai.GenerativeModel('gemini-pro')

# select to use OpenAI's text to speech API
openaitts = True    

def speak_text(text):
    global openaitts    

    if openaitts:

        response = client.audio.speech.create(
            model="tts-1",
            # alloy: man; nova: woman
            voice="nova",
            input= text )
        
        fname = 'output.mp3'
        mp3file =open(fname, 'w+')  
                      
        response.write_to_file(fname)

        try:        
            pygame.mixer.music.load(mp3file)
            pygame.mixer.music.play()
        
            while pygame.mixer.music.get_busy():
                #
                time.sleep(0.25)
            
            pygame.mixer.music.stop()    
            mp3file.close()
        
        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            mp3file.close()
            #print("\nAudio playback stopped.")
    else:
        engine.say(text)
        # print("AI: " + text)
        engine.runAndWait()
        
talk = []

# save conversation to a log file 
def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a") as f:
        f.write(text + "\n")

# Main function for conversation
def main():
    global talk, today, model  
    
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold=False
    rec.energy_threshold = 400    
    
    sleeping = True 
    
    while True:     
        
        with mic as source1:            
            rec.adjust_for_ambient_noise(source1, duration= 0.5) # type: ignore

            print("Listening ...")
            
            try: 
                audio = rec.listen(source1, timeout = 10, phrase_time_limit = 15)
               
                text = rec.recognize_google(audio) # type: ignore
                
                # AI is in sleeping mode
                if sleeping == True:
                    # User must start the conversation with the wake word "Jack"
                    # This word can be chagned by the user. 
                    if "jack" in text.lower():
                        request = text.lower().split("jack")[1]
                        
                        sleeping = False
                        # AI is awake now, 
                        # start a new conversation 
                        append2log(f"_"*40)
                        talk = []                        
                        today = str(date.today()) 
                        
                        # if the user's question is none or too short, skip 
                        if len(request) < 5:
                            speak_text("Hi, there, how can I help?")
                            append2log(f"AI: Hi, there, how can I help? \n")
                            continue                      

                    # if user did not say the wake word, nothing will happen 
                    else:
                        continue
                      
                # AI is awake         
                else: 
                    
                    request = text.lower()

                    if "that's all" in request:
                                               
                        append2log(f"You: {request}\n")
                        
                        speak_text("Bye now")
                        
                        append2log(f"AI: Bye now. \n")                        

                        print('Bye now')
                        
                        sleeping = True
                        # AI goes back to speeling mode
                        continue
                    
                    if "jack" in request:
                        request = request.split("jack")[1]                        
                
                # process user's request (question)
                append2log(f"You: {request}\n ")

                print(f"You: {request}\n AI: " )

                talk.append({'role':'user', 'parts':[request]} )

                response = model.generate_content(talk, stream=True,
                #generation_config=genai.types.GenerationConfig(
                # Only one candidate for now.
                #max_output_tokens=125) 
                )

                for chunk in response:
                    print(chunk.text, end='') 
                    speak_text(chunk.text.replace("*", ""))

                #print(response.text)
                #speak_text(response.text.replace("*", ""))
                print('\n')
                talk.append({'role':'model', 'parts':[response.text]})
                
                #print(talk[-1]['parts'][0])                

                append2log(f"AI: {response.text } \n")
 
            except Exception as e:
                continue 
 
if __name__ == "__main__":
    main()
