import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import urllib.parse
import pywhatkit
import pyjokes
import time
import os
import pyautogui
import random

# Initialize and configure pyttsx3 voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you?")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio, language='en-US')
        print("You said:", command)
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, there was a problem with the service.")
        return ""
    return command.lower()

def search_google(query):
    speak(f"Searching Google for {query}")
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def play_music_youtube(song_name):
    speak(f"Playing {song_name} on YouTube.")
    pywhatkit.playonyt(song_name)

def open_cricbuzz():
    speak("Opening Cricbuzz for live cricket updates.")
    webbrowser.open("https://www.cricbuzz.com")

def tell_joke():
    joke = pyjokes.get_joke()
    speak("Here's a joke for you...")
    time.sleep(0.8)
    speak(joke)

# Open common PC apps
def open_application(command):
    if "notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in command:
        speak("Opening Calculator")
        os.system("calc")
    elif "chrome" in command:
        speak("Opening Google Chrome")
        os.system("start chrome")
    else:
        speak("Sorry, I don't know how to open that application.")

# Take screenshot
def take_screenshot():
    speak("Taking a screenshot now.")
    screenshot = pyautogui.screenshot()
    filename = f"screenshot_{int(time.time())}.png"
    screenshot.save(filename)
    speak(f"Screenshot saved as {filename}")

# Motivation Quotes
def motivate():
    quotes = [
        "Believe in yourself and all that you are.",
        "Every day is a new beginning.",
        "Success is not final, failure is not fatal.",
        "Push yourself because no one else is going to do it for you.",
        "You are capable of amazing things."
    ]
    quote = random.choice(quotes)
    speak("Here's your motivation.")
    time.sleep(0.5)
    speak(quote)

# News headlines
def news_headlines():
    speak("Fetching latest news headlines.")
    pywhatkit.search("latest news headlines India")

def main():
    greet()
    while True:
        command = listen()

        if "wikipedia" in command:
            speak("Searching Wikipedia...")
            topic = command.replace("wikipedia", "").strip()
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except Exception:
                speak("Sorry, I could not find information about that.")

        elif "search google for" in command:
            query = command.replace("search google for", "").strip()
            if query:
                search_google(query)
            else:
                speak("Please tell me what you want to search for.")

        elif "open google" in command:
            webbrowser.open("https://www.google.com")
            speak("Opening Google.")

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        elif "play" in command and "on youtube" in command:
            song_name = command.replace("play", "").replace("on youtube", "").strip()
            if song_name:
                play_music_youtube(song_name)
            else:
                speak("Please tell me what song you'd like to hear.")

        elif "cricket score" in command or "match update" in command:
            speak("Here is the latest cricket score.")
            pywhatkit.search("live cricket score")

        elif "cricket" in command:
            open_cricbuzz()

        elif "tell a joke" in command or "joke" in command:
            tell_joke()

        elif "open" in command and "application" in command:
            open_application(command)

        elif "screenshot" in command:
            take_screenshot()

        elif "motivate me" in command or "motivation" in command or "quote" in command:
            motivate()

        elif "news" in command or "headlines" in command:
            news_headlines()

        elif "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye!")
            break

        elif command != "":
            speak("You can ask me to open apps, take screenshots, give a quote, tell a joke, or search the internet.")

if __name__ == "__main__":
    main()
