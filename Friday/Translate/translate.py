import pyttsx3
import speech_recognition as sr
import webbrowser
import pywhatkit
import wikipedia
import os
import pyautogui
import keyboard
import pyjokes
import datetime
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Tk
from tkinter import StringVar
from pytube import YouTube
from playsound import playsound

Assistant = pyttsx3.init('sapi5')
voices = Assistant.getProperty('voices')
Assistant.setProperty('voices',voices[0].id)
Assistant.setProperty('rate',190)

def Speak(audio):
    print("   ")
    Assistant.say(audio)
    print("   ")
    Assistant.runAndWait()
    
def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am Listining")
        command.pause_threshold = 1
        audio = command.listen(source)
        
        try:
            print("Recognizing.....")
            query = command.recognize_google(audio,language='en-in')
            print(f"you said:{query}")
            
        except Exception as Error:
            return "none"
        
        return query.lower()
    