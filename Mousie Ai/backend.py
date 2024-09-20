import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
from ecapture import ecapture as ec
from groq import Groq

# Set up GROQ API
GROQ_API_KEY = "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"  # Replace with your GROQ API key

client = Groq(api_key=GROQ_API_KEY)

print('Loading your AI personal assistant - Mousie')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

def generate_groq_response(query):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        print("API Response:", response)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "I couldn't generate a response."

def generate_response(prompt):
    response = generate_groq_response(prompt)
    return response

if __name__ == "__main__":
    wishMe()
    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        response = generate_groq_response(statement)
        speak(response)
        if statement == "none":
            continue
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Your personal assistant Mousie is shutting down, goodbye')
            break
        # Other commands can be handled here as needed