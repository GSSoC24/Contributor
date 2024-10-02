import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

print("Initializing Jarvis")

machine = pyttsx3.init()
listener = sr.Recognizer()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    global instruction
    try: 
        with sr.Microphone() as origin:
            print("listening....")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)     # type: ignore
            instruction = instruction.lower()
            if "jarvis" in instruction:
              instruction = instruction.replace("jarvis"," ")
              print(instruction)

    except:
       pass

    return instruction

def play_Jarvis():
    while True:
        instruction = input_instruction()
        print(instruction)
        if "play" in instruction:
            song = instruction.replace('play',"")
            talk("playing " + song)
            pywhatkit.playonyt(song)  # type: ignore      

        elif 'time' in instruction:  
            time = datetime.datetime.now().strftime('%I:%M%p')
            talk('Current time is ' + time)

        elif 'date' in instruction: 
             date = datetime.datetime.now().strftime('%d /%m /%Y')
             talk("Today's date is " + date)

        elif 'how are you' in instruction: 
           talk('I am fine, how are you')

        elif 'what is your name' in instruction: 
            talk('I am Jarvis, what can I do for you ?')

        elif 'who built you' in instruction: 
           talk('I was build by Nithin')

        elif 'who is nitin' in instruction: 
           talk('nithin is an passionate software engineer 1') 

        elif 'what is software testing' in instruction: 
           talk('Software testing is the process of evaluating and verifying that a software application or system meets the required specifications, user expectations, and industry standards. It involves identifying and reporting defects or bugs in the software, and ensuring that the software is reliable, stable, and performs as expected.')  
           
        elif 'what is artifical intelligence' in instruction: 
          talk('Artificial Intelligence (AI) refers to the development of computer systems that can perform tasks that typically require human intelligence')  
                   
        elif 'What is selenium' in instruction:
            talk('selenium is an test automation tool which is used for scrum methodologies and it is an test automation tool for the automation of the websites and the python libraries for the selenium pip install selenium')
          
           
        elif 'who is' in instruction:
            human = instruction.replace('who is'," ")
            try:
                info = wikipedia.summary(human, 1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk("There are multiple results for " + human)
            except wikipedia.exceptions.PageError:
                talk("I couldn't find any information on " + human)
    
        else:
            talk('please repeat')    


play_Jarvis()