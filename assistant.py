from flask import Flask, render_template, request
import speech_recognition as sr
import playsound
from gtts import gTTS
import os
import wolframalpha # to calculate strings into formula
import pyttsx3
import datetime
import time
from selenium import webdriver # to control browser operations
import subprocess



app = Flask(__name__)


num = 1
def assistant_speaks(output):
    global num
    num += 1
    print("Peter : ", output)
    toSpeak = gTTS(text = output, lang ='en', slow = False)
    file = str(num)+".mp3"
    toSpeak.save(file)
    playsound.playsound(file, True)
    os.remove(file)


def get_audio():
    rObject = sr.Recognizer()
    audio = ''
    with sr.Microphone() as source:
        print("Listening...")
        audio = rObject.listen(source, phrase_time_limit = 5)
    try:
        print("Processing...")
        text = rObject.recognize_google(audio, language ='en-US')
        print("You : ", text)
        return text
    except:
        print("Restarting")
        # assistant_speaks("Dont mumble, speak up")
        return 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/1')
def index1():
    return render_template('assistant.html')


@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio = request.files['audio']
    audio.save('audio.webm')

    # Convert WebM audio file to WAV format
    subprocess.run(['ffmpeg', '-i', 'audio.webm', 'audio.wav'], capture_output=True)

    # Perform speech recognition on the converted audio file
    r = sr.Recognizer()
    with sr.AudioFile('audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='en-US')

    # Process the recognized text
    if text == 'hello':
        assistant_speaks('Oh hello')
    elif 'stop' in text.lower():
        assistant_speaks('Peter Out')
    else:
        assistant_speaks('huh, Dont mumble')
    # Remove the audio files
    os.remove('audio.webm')
    os.remove('audio.wav')
    return 'Done'


if __name__ == '__main__':
    app.run()
