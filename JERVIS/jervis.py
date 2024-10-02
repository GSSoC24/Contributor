import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib

print("Initializing Jarvis")

MASTER = "Nithin"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

#speak function will pronounce the string which is passed to it
def speak(text):
    engine.say(text) 
    engine.runAndWait()

# This function will wish you as per the current time
def WishMe():
    hour = int(datetime.datetime.now().hour)
    

    if hour>=0 and hour <12:
        speak("Good morning " + MASTER)

    elif hour>=12 and hour<18:
        speak("Good Afternoon " + MASTER)    

    else:
        speak("Good Evening " + MASTER)    

    speak("I am Jarvis. How may I help You?")

#This command will take commad from the microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try : 
        print("Recognizing...")
        query = r.recognize_google(audio, language ='en-in')   # type: ignore
        print(f"user said:{query}\n")
        return query.lower()  

    except Exception as e:
        print("say that again please")
        return "None"  

# Main Program Starts Here..
speak("Initializing Jarvis.....")
WishMe()
query = takeCommand()

#logic for executing basic tasks as per the query
if query!= "none":
    if 'wikipedia' in query: #
        speak('searching wikipedia...')
        query = query.replace("wikipedia","") 
        results = wikipedia.summary(query, sentences =2)
        print(results)
        speak(results)

elif 'open Youtube' in query: 
    # webbrowser.open("youtube.com")
    url = ("https://www.youtube.com/") 
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe %s"
    webbrowser.get(chrome_path).open(url)

elif 'open Google' in query: 
    # webbrowser.open("youtube.com")
    url = ("https://www.google.com/") 
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe %s"
    webbrowser.get(chrome_path).open(url)

elif 'open reddit' in query: 
    # webbrowser.open("youtube.com")
    url = ("https://www.reddit.com/") 
    chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe %s"
    webbrowser.get(chrome_path).open(url)   

elif 'play music' in query.lower():
    songs = os.listdir()