from flask import Flask, render_template, request
import speech_recognition as sr
import playsound
from gtts import gTTS
import os
import wolframalpha # to calculate strings into formula
import datetime
import time
from selenium import webdriver # to control browser operations
import subprocess

import wikipedia
import webbrowser
from twilio.rest import Client
from clint.textui import progress
# from ecapture import ecapture as ec
from bs4 import BeautifulSoup
# import win32com.client as wincl
from urllib.request import urlopen


app = Flask(__name__)


num = 1
def assistant_speaks(output):
    global num
    num += 1
    print("Emily : ", output)
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


def greeting():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        assistant_speaks("Good Morning Sir !")
    elif hour>= 12 and hour<18:
        assistant_speaks("Good Afternoon Sir !")  
    else:
        assistant_speaks("Good Evening Sir !") 
    assistant_speaks("I am Emily your online Assistant")


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()


def delete_audio_files():
    if os.path.exists("audio.webm"):
        os.remove("audio.webm")
        # print("Deleted audio.webm")
    if os.path.exists("audio.wav"):
        os.remove("audio.wav")
        # print("Deleted audio.wav")


def clear():
    os.system('clear')


def process_request(text):
    # All the requests by user will be stored here in 'text'
    try:
        if 'hello' in text.lower():
            assistant_speaks("Do you want something or are you just going to annoy me?")

        else:
            assistant_speaks("Please speak up, Don't mumble")

    except sr.UnknownValueError:
        assistant_speaks('Sorry, I could not understand what you said.')
    except sr.RequestError:
        assistant_speaks('Sorry, there was an issue with the speech recognition service.')
    except Exception as e:
        assistant_speaks(f'Sorry, an error occurred: {str(e)}')

    return 'Done'


@app.route('/')
def index():
    assistant_speaks("Emily's Now Online")
    return render_template('index.html')


@app.route('/1')
def index1():
    return render_template('assistant.html')


@app.route('/process_audio', methods=['POST'])
def process_audio():
    delete_audio_files()
    audio = request.files['audio']
    audio.save('audio.webm')

    # Convert WebM audio file to WAV format
    # subprocess.run(['ffmpeg', '-i', 'audio.webm', 'audio.wav'], capture_output=True)
    subprocess.run(['ffmpeg', '-i', 'audio.webm', 'audio.wav'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        r = sr.Recognizer()
        with sr.AudioFile('audio.wav') as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='en-US')
            
            if text:
                # Process the recognized text
                print("Recognized text:", text)
            else:
                print("No input detected.")
                
    except sr.UnknownValueError:
        assistant_speaks('Sorry, Unable to recognize speech.')
        delete_audio_files()
        print(sr.UnknownValueError)
    except sr.RequestError as e:
        print("Error occurred during speech recognition:", str(e))
        assistant_speaks('Sorry, there was an issue with the speech recognition service.')
        delete_audio_files()
    except Exception as e:
        assistant_speaks(f'Sorry, an exception error occurred: {str(e)}')
        delete_audio_files()
        print({str(e)})

    try:
        if 'hello' in text.lower():
            greeting()

        elif 'open youtube' in text.lower() or 'youtube' in text.lower():
            assistant_speaks("Here you go to YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in text.lower() or 'google' in text.lower():
            assistant_speaks("Here you go to Google")
            webbrowser.open("https://www.google.com")

        elif 'open stackoverflow' in text.lower():
            assistant_speaks("Here you go to Stack Overflow. Happy coding!")
            webbrowser.open("https://www.stackoverflow.com")

        elif 'what is the time' in text.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            assistant_speaks(f"Sir, the time is {strTime}")

        elif 'wikipedia' in text.lower() or 'wiki' in text.lower():
            assistant_speaks('Searching Wikipedia...')
            query = text.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 5)
            speak = "According to Wikipedia " + results
            assistant_speaks(speak)

        elif 'repeat' in text.lower() or 'copy cat' in text.lower():
            assistant_speaks(text)

        # add requests here


        else:
            assistant_speaks("This is what I heard, " + text)
            # assistant_speaks("Speak up, Don't mumble")
            assistant_speaks("Please try another request")
            delete_audio_files()

    except sr.UnknownValueError:
        assistant_speaks('Sorry, I could not understand what you said.')
        delete_audio_files()
        print(sr.UnknownValueError)
    except sr.RequestError:
        assistant_speaks('Sorry, there was an issue with the speech recognition service.')
        delete_audio_files()
        print(sr.UnknownValueError)
    except Exception as e:
        assistant_speaks(f'Sorry, an error occurred: {str(e)}')
        delete_audio_files()
        print({str(e)})

    delete_audio_files()
    
    return 'Done'


if __name__ == '__main__':
    clear()
    delete_audio_files()
    app.run()
