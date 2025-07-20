import speech_recognition as sr
import pyttsx3
import webbrowser
import threading
import http.server
import socketserver
import requests
import os
import time

# Setup
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print(f"FRIDAY: {text}")
    engine.say(text)
    engine.runAndWait()

# Start glowing orb UI
def launch_ui():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Launching Orb UI...")
        httpd.serve_forever()

# Listen to command
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = r.listen(source, phrase_time_limit=4)
            text = r.recognize_google(audio).lower()
            print("User said:", text)
            return text
        except:
            speak("Sorry, say that again.")
            return ""

# Weather
def get_weather():
    city = "Delhi"
    key = "686d487ae00c37f15964bc0bcba6b953"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    try:
        res = requests.get(url).json()
        if "main" in res:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            speak(f"In {city}, it's {temp}°C with {desc}.")
        else:
            speak("Weather not found.")
    except:
        speak("Could not get weather.")

# News
def get_news():
    key = "70678a9afa6343a2b6367f4dc79963d2"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={key}"
    try:
        res = requests.get(url).json()
        articles = res.get("articles", [])[:5]
        if articles:
            speak("Top headlines are:")
            for i, a in enumerate(articles, 1):
                speak(f"{i}. {a['title']}")
        else:
            speak("No news found.")
    except:
        speak("News service failed.")

# Main loop
def friday():
    while True:
        wake = listen()
        if "friday" in wake:
            speak("Yes buddy")
            command = listen()

            if "weather" in command:
                get_weather()
            elif "news" in command:
                get_news()
            elif "youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com")
            elif "play" in command:
                song = command.replace("play", "")
                speak(f"Playing {song}")
                import pywhatkit
                pywhatkit.playonyt(song)
            elif "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand.")
        else:
            print("Wake word not detected.")

# Run everything
if __name__ == "__main__":
    # Start orb UI
    threading.Thread(target=launch_ui, daemon=True).start()
    webbrowser.open("http://localhost:8000/front.html")
    speak("Initializing FRIDAY...")
    friday()
