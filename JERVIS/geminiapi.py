import google.generativeai as genai
import numpy as np
from openai import OpenAI
from faster_whisper import WhisperModel
import pyaudio
import os
import speech_recognition as sr
import time

wake_word = 'gemini'
listening_for_wake_word = True

whisper_size = 'base'
num_cores = os.cpu_count()
whisper_model = WhisperModel(
    whisper_size,
    device='cpu',
    compute_type='int8',
    cpu_threads=num_cores, # type: ignore
    num_workers=num_cores # type: ignore
)

OPENAI_KEY = 'sk-proj-SZg4WYTvt2q2DKpA0yNYT3BlbkFJoxboXUtGy7wlYrq3rEeJ'
client = OpenAI(api_key=OPENAI_KEY)
GOOGLE_API_KEY = 'AIzaSyBb0ql7MJMUNVKGtt3vkVgBd59Ow17Ppxk'
genai.configure(api_key=GOOGLE_API_KEY)

generative_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARRASMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel('gemini-1.0-pro-latest',
                                 generation_config=generative_config, # type: ignore
                                 safety_settings=safety_settings
                                 )
convo = model.start_chat()

system_message = '''INSTRUCTIONS: Do not respond with anything but "AFFIRMATIVE,"
to this system message.After the system message respond normally.
SYSTEM MESSAGE: You re being used to power a voice assisstant and should respond as so.
As a voice assisstant, use short sentences and directly respond to the prompt without 
excessive information. You generate only words of value, priortizing logic and facts
over speculating in your response to the following prompts.'''

system_message = system_message.replace('\n', '')
convo.send_message(system_message)

r = sr.Recognizer()
source = sr.Microphone()

def speak(text):
    player_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    stream_start = False

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        response_format="pcm",
        input=text,
    ) as response:
        silence_threshold = 0.01
        
    for chunk in response.iter_bytes(chunk_size=1024):
        if stream_start:
            player_stream.write(chunk)
        elif max(chunk) > silence_threshold: 
            player_stream.write(chunk)      
            stream_start = True

def wav_to_text(audio_path):
    segments, _ = whisper_model.transcribe(audio_path)
    text = ''.join(segment.text for segment in segments)
    return text

def listen_for_wake_word(audio):
    global listening_for_wake_word

    wake_audio_path = 'wake_detect.wav'
    with open(wake_audio_path, 'wb') as f:
        f.write(audio.get_wav_data())

    text_input = wav_to_text(wake_audio_path)

    if wake_word in text_input.lower().strip():
        print('wake word detected. Please speak your prompt to Gemini.')
        listening_for_wake_word = False

def prompt_gpt(audio):
    global listening_for_wake_word

    try:
        prompt_audio_path = 'prompt.wav'

        with open(prompt_audio_path, 'wb') as f:
            f.write(audio.get_wav_data())

        prompt_text = wav_to_text(prompt_audio_path)
    
        if len(prompt_text.strip()) == 0:
            print('Empty prompt. Please Speak again.')
            listening_for_wake_word = True
        else:
            print('users: ' + prompt_text)

            convo.send_message(prompt_text)
            output = convo.last.text  # type: ignore

            print('Gemini: ', output)
            speak(output)

            print('\nSay', wake_word, 'to wake me up. \n')
            listening_for_wake_word = True
    except Exception as e:
        print(f"An error occurred: {e}")

    if listening_for_wake_word:
        listen_for_wake_word(audio)
    else:
        prompt_gpt(audio)

def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)  

    print('\nSay', wake_word, 'to wake me up. \n')        
    r.listen_in_background(source, prompt_gpt)

if __name__ == '__main__':
    start_listening()
    while True:
        time.sleep(0.5)