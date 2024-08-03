import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

recognizer = sr.Recognizer()  # Define Recognizer instance globally

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return ""
    except sr.RequestError as e:
        print(f"Error requesting recognition from Google Speech Recognition service: {e}")
        return ""

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Replace 'your_email' and 'your_password' with your actual Gmail credentials
    server.login('your_email', 'your_password')
    server.sendmail('your_email', to, content)
    server.close()

def wish():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("How may I help you")

if __name__ == "__main__":
    speak("This is FRIDAY")
    wish()

    while True:
        query = takecommand()

        if "open notepad" in query:
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")


        #elif "play music" in query:
           # os.system(f"open\\Apps\\Spotify Music.app")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "open youtube" in query:
            speak("Sir, what should I search on youtube?")
            search_query = takecommand()
            webbrowser.open(f"https://www.youtube.com/search?q={search_query}")

        elif "open linkedin" in query:
            webbrowser.open("www.linkedin.com")

        elif "open stack overflow" in query:
            webbrowser.open("stackoverflow.com")

        elif "open chess" in query:
            webbrowser.open("www.chess.com")

        elif "open google" in query:
            speak("Sir, what should I search on Google?")
            search_query = takecommand()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "play songs on youtube" in query:
            kit.playonyt("hislerim")

        elif "email to brijesh" in query:
            try:
                speak("What should I say?")
                content = takecommand()
                to = "brijesh@example.com"  # Replace with recipient's email address
                sendEmail(to, content)
                speak("Email has been sent to Brijesh")
            except Exception as e:
                print(e)
                speak("Sorry sir, I am not able to send this mail to Brijesh")

        elif "no thanks" in query:
            speak("Thanks for using me sir, have a good day.")
            sys.exit()
