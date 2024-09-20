import ctypes
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
from ecapture import ecapture as ec
from groq import Groq
import pyautogui
from pynput import keyboard

# Set up GROQ API
GROQ_API_KEY = "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"  # Replace with your GROQ API key
client = Groq(api_key=GROQ_API_KEY)

# Initialize the Tkinter window
class VoiceInputApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Input Display")
        self.label = tk.Label(self.root, text="", wraplength=400, justify="left")
        self.label.pack(padx=20, pady=20)
        self.root.geometry("400x200")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.withdraw()  # Hide the window initially

    def show(self, text):
        self.label.config(text=text)
        self.root.deiconify()  # Show the window
        self.resize_window(text)
        self.update_position()  # Update position based on cursor

    def hide(self):
        self.root.withdraw()

    def resize_window(self, text):
        num_lines = text.count('\n') + 1
        char_count = len(text)
        new_height = min(max(200, num_lines * 20 + 60), 600)
        new_width = min(max(400, char_count * 7), 600)
        self.root.geometry(f"{new_width}x{new_height}")

    def update_position(self):
        x, y = pyautogui.position()
        self.root.geometry(f"+{x + 10}+{y + 10}")
        self.root.after(50, self.update_position)

    def speak(self, text):
        engine = pyttsx3.init('sapi5')
        engine.say(text)
        engine.runAndWait()

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            self.speak("Hello, Good Morning")
        elif hour < 18:
            self.speak("Hello, Good Afternoon")
        else:
            self.speak("Hello, Good Evening")

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.show("Listening...")
            audio = r.listen(source)
            try:
                statement = r.recognize_google(audio, language='en-in')
                return statement.lower()
            except Exception:
                self.speak("Pardon me, please say that again")
                return "none"

    def generate_groq_response(self, query):
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            return "I couldn't generate a response."

# Global hotkey handler
def on_press(key):
    try:
        if key == keyboard.Key.shift and keyboard.Controller().pressed(keyboard.Key.ctrl_l) and keyboard.Controller().pressed('q'):
            app.wish_me()
            statement = app.take_command()
            if statement == "none":
                return
            response = app.generate_groq_response(statement)
            app.show(response)
            app.speak(response)

        elif key == keyboard.Key.esc:
            app.hide()
    except AttributeError:
        pass

# Main program
if __name__ == "__main__":
    app = VoiceInputApp()

    # Start global hotkey listener
    with keyboard.Listener(on_press=on_press) as listener:
        app.root.mainloop()
        listener.join()