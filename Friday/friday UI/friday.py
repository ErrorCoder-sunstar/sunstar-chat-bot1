import operator
import time
import webbrowser
import numpy as np
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import pywhatkit as kit
import smtplib
import sys
import pyjokes
from geopy.geocoders import Nominatim
import geocoder
import pywhatkit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

NEWS_API_KEY = "" # Replace with your API key
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
# print((voices[1].id))
engine.setProperty("voices", voices[1].id)
# engine.setProperty('rate', 180-200)


# text to speach
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# to convert voice into text
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=120, phrase_time_limit=10)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")

    except Exception as e:
        # speak('say that again please...')
        return "none"
    query = query.lower()
    return query


# 1.to get weather
def get_weather(city_name):
    API_KEY = (
        ""  # Replace with your OpenWeatherMap API key
    )
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        weather_description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        return f"Weather in {city_name}: {weather_description}, Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s"
    else:
        return "Failed to fetch weather data."


# 2.to speak weather
def get_and_speak_weather_in_location():
    city_name = (
        "Chennai, IN"  # Replace with your city and country name, e.g., "New York, US"
    )
    weather_info = get_weather(city_name)
    speak(weather_info)


# 3.to greet
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"Good morning master I am friday your virtual assistant, now its {tt} ")
    elif hour > 12 and hour < 16:
        speak(
            f"Good afternoon master i am friday your virtual assistant, now its {tt} "
        )
    else:
        speak(f"good evening master i am friday your virtual assistant, now its {tt} ")

    get_and_speak_weather_in_location()

    speak("Ready for your orders sir")


# 4.to send email
def sendEmail(to, content):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("your mail id", "your password")
    server.sendmail("your mail id", to, content)
    server.close()


# 5.to fetch news
def get_news():
    params = {
        "apiKey": NEWS_API_KEY,
        "country": "in",
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        news_data = response.json()
        headlines = []  # List to store the top 10 headlines
        for article in news_data["articles"]:
            if len(headlines) >= 10:  # Stop after getting 10 headlines
                break

            title = article["title"]
            source = article["source"]["name"]
            headline = f"{source}: {title}"
            headlines.append(headline)

        # Print all the top 10 headlines
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline}")

        # Speak out the top 10 headlines
        speak_headlines(headlines)
    else:
        print("Failed to retrieve news data.")


# 6.to speak headline
def speak_headlines(headlines):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties (optional)
    # For example, you can set the speech rate (default is 200)
    engine.setProperty("rate", 180)  # Speed up to 180 words per minute

    # Speak each headline one by one with a delay between each headline
    for headline in headlines:
        speak_text(headline)
        time.sleep(2)  # Add a delay of 2 seconds between headlines


# 7.to speak the text of news headline
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)
    engine.say(text)
    engine.runAndWait()


# 8.to get exact location
def get_location():
    # Get your current coordinates using the 'geocoder' library
    g = geocoder.ip("me")
    latitude, longitude = g.latlng

    # Use the OpenStreetMap Nominatim API to get the location details
    geolocator = Nominatim(user_agent="location_app")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)

    if location:
        print("sir i am not sure but we are exactly located at:")
        speak(location)
    else:
        print("Due to network error Location not found sir sorry.")


# 9.to open prensetation
def open_presentation():
    presentation_path = "D:\\Sunny-OOPs.pptx"
    os.startfile(presentation_path)
    speak("Presentation opened successfully.")


# 10.to shut down the system
def shut_down_system():
    speak("Are you sure you want to shut down the system?")
    response = takecommand().lower()
    if "yes" in response:
        speak("Shutting down the system. Goodbye!")
        os.system("shutdown /s /t 1")  # Shutdown the system after 1 second delay
    else:
        speak("Okay, I will not shut down the system.")


# 11.to sleep the system
def sleep_system():
    speak("Are you sure you want to put the system to sleep?")
    response = takecommand().lower()
    if "yes" in response:
        speak("Putting the system to sleep. Goodbye!")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        speak("Okay, I will not put the system to sleep.")


# 12.to restart the system
def restart_system():
    speak("Are you sure you want to restart the system?")
    response = takecommand().lower()
    if "yes" in response:
        speak("Restarting the system. Goodbye!")
        os.system("shutdown /r /t 1")  # Restart the system after 1 second delay
    else:
        speak("Okay, I will not restart the system.")


#13. to open youtube
def open_youtube():
    webbrowser.open("https://www.youtube.com")
    speak("YouTube is now open.")


# 14.to close youtube
def close_youtube():
    os.system("TASKKILL /F /IM chrome.exe /T")  # Close all Chrome processes
    speak("YouTube is now closed.")


# 15.to close chrome
def close_chrome():
    os.system("TASKKILL /F /IM chrome.exe /T")  # Close all Chrome processes
    speak("Chrome is now closed.")


# 16.to close excel
def close_excel():
    os.system("taskkill /f /im excel.exe")
    speak("Microsoft Excel is now closed.")


# 17.to close word
def close_word():
    os.system("taskkill /f /im winword.exe")
    speak("Microsoft Word is now closed.")


# 18.to close power point
def close_powerpoint():
    os.system("taskkill /f /im powerpoint.exe")
    speak("Microsoft PowerPoint is now closed.")
    
#19.password protected 
def Pass(pass_inp):
    password = "Isha"
    passss = str(pass_inp)
    
    if passss == str(pass_inp):
        speak("password Matched")
        speak("welcome master Sun star")
    else:
        speak("password Not Matched clarify your access with sun star")
        sys.exit()

def TaskExecution():
    wish()

    while True:
        # if 1:

        query = takecommand().lower()

        # logic building for task
        #19.
        if "friday open notepad" in query:
            dpath = "C:\\Windows\\System32\\notepad.exe"
            os.startfile(dpath)

        elif "friday shutdown" in query:
            shut_down_system()

        elif "friday screen off" in query:
            sleep_system()

        elif "friday restart" in query:
            restart_system()

        elif "friday open youtube" in query:
            open_youtube()

        elif "friday close youtube" in query:
            close_youtube()

        elif "friday open presentation" in query:
            open_presentation()
        #20
        elif "friday open my linkedin profile" in query:
            webbrowser.open("www.linkedin.com/in/benedict-sunny-paul-391528261/")
        #21
        elif "friday open my dark profile" in query:
            webbrowser.open("www.github.com/ErrorCoder-sunstar")
        #22
        elif "friday open world" in query:
            webbrowser.open("https://chat.openai.com/")
        #23
        elif "friday open chrome" in query:
            cpath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome"
            os.startfile(cpath)
        
        elif "friday close chrome" in query:
            close_chrome()

        elif "friday open excel" in query:
            cpath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel"
            os.startfile(cpath)

        elif "friday close excel" in query:
            close_excel()

        elif "friday open word" in query:
            cpath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word"
            os.startfile(cpath)

        elif "friday close word" in query:
            close_word()

        elif "friday open powerpoint" in query:
            cpath = (
                "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint"
            )
            os.startfile(cpath)

        elif "friday close powerpoint" in query:
            close_powerpoint()

        elif "friday open brackets" in query:
            cpath = (
                "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Brackets"
            )
            os.startfile(cpath)

        elif "wikipedia" in query:
            speak("searching in wikipedia.....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            # print(results)

        elif "friday search in google" in query:
            speak("master , ask me your query let me search and show the results ")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "friday send message" in query:
            kit.sendwhatmsg("+917010984429", "this is just testing message", 23, 14)

        elif "friday say my ip address" in query:
            ip = get("https://api.ipify.org").text
            speak(f"Your IP address is {ip}")

        elif "friday play my favourite vijay song from youtube" in query:
            kit.playonyt("Naa Ready Lyric Video")

        elif "friday play my favourite rajini song from youtube" in query:
            kit.playonyt("Thalaivar Alappara")

        # elif "friday send email to h1" in query:
        # try:
        # speak("what should i say?")
        # content = takecommand().lower()
        # to = "imman042@gmail.com"
        # sendEmail(to, content)
        # speak("Email has been sent to avi sir")

        # except Exception as e:
        # print(e)
        # speak("sorry sir i am unable to sent the mail this time")

        # elif "thank you friday take rest" in query:
        # speak("welcome master always here for you at any time ")
        # sys.exit()

        elif "friday close notepad" in query:
            speak("okay sir , i am closing it")
            os.system("taskkill/f /im notepad.exe")

        elif "friday set alarm" in query:
            nn = int(datetime.datetime.now().hour)
            if nn == 19:
                music_dir = "D:\\music"
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))

        elif "friday tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "friday switch to next show" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "friday what is going on around me" in query:
            speak("please wait sir,looking for latest news around you")
            get_news()

        elif "friday locate me now" in query:
            speak("Tracing your location sir .....")
            get_location()

        elif "friday open vs code" in query:
            fpath = "C:\\Users\\pbene\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
            os.startfile(fpath)

        elif "friday calculate this for me" in query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("yes sure say me the sum")
                # print("listening....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)

            def get_operator_fn(op):
                return {
                    "+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.__truediv__,
                }[op]

            def eval_binary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)

            speak("your result is")
            speak(eval_binary_expr(*(my_string.split())))

        elif "take rest friday" in query:
            speak("okay master, you can call me anytime")
            break

        elif "friday connect with internet" in query:
            from pywikihow import search_wikihow

            speak("Conneted with internet sir")
            while True:
                speak("say me what you want to know about")
                how = takecommand()
                try:
                    if "disconnect" in how:
                        speak("done master, disconnected from internet")
                        break
                    else:
                        max_results = 1
                        how_to = search_wikihow(how, max_results)
                        assert len(how_to) == 1
                        how_to[0].print()
                        speak(how_to[0].summary)
                except Exception as e:
                    speak("sorry sir i am unable to find this")

        elif "friday how much power left in our system" in query:
            import psutil

            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"sir power left in our system is{percentage} ")

        elif "friday raise up" in query:
            pyautogui.press("volumeup")

        elif "friday drop down" in query:
            pyautogui.press("volumedown")

        elif "friday silent" in query:
            pyautogui.press("volumemute")

        elif "friday spy on" in query:
            import urllib.request
            import cv2
            import time

            URL = "http://192.168.29.88:8080/shot.jpg"
            while True:
                img_arr = np.array(
                    bytearray(urllib.request.urlopen(URL).read()), dtype=np.uint8
                )
                img = cv2.imdecode(img_arr, -1)
                cv2.imshow("IPWebcam", img)
                q = cv2.waitKey(1)
                if q == ord("q"):
                    break
            cv2.destroyAllWindows()
        
        


if __name__ == "__main__":
    speak("This assistant is locked by our master so kindly provide the passkey for accessing me")
    passss = input("enter the passkey:")
    Pass(passss)
    while True:
        permission = takecommand()
        if "wake up friday" in permission:
            TaskExecution()
        elif "goodbye friday" in permission:
            speak("bye have a good day")
            sys.exit()
