import ctypes
import speech_recognition as sr
from pynput import keyboard
import tkinter as tk
import pyautogui  # For getting mouse position
import subprocess
import backend  # Import the backend module

# Initialize the tkinter window
class VoiceInputApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Input Display")
        self.label = tk.Label(self.root, text="", wraplength=400, justify="left")
        self.label.pack(padx=20, pady=20)
        self.root.geometry("400x200")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.withdraw()  # Hide the window initially

    def show(self, prompt, response=None):
        text = prompt
        if response:
            text += f"\n\nResponse: {response}"
        
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
        x, y = pyautogui.position()  # Get current mouse position
        self.root.geometry(f"+{x + 10}+{y + 10}")  # Offset slightly from cursor
        self.root.after(50, self.update_position)  # Update position every 50 ms

# Load and set the custom cursor
def load_custom_cursor(cursor_path):
    cursor = ctypes.windll.user32.LoadCursorFromFileW(cursor_path)
    if cursor == 0:
        print("Failed to load the cursor. Check the file path and format.")
    else:
        ctypes.windll.user32.SetSystemCursor(cursor, 32512)  # Default pointer

# Voice recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        app.show("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error in the voice recognition service."

# Global hotkey handler
def on_press(key):
    try:
        if key == keyboard.Key.shift and keyboard.Controller().pressed(keyboard.Key.ctrl_l) and keyboard.Controller().pressed('q'):
            load_custom_cursor(r"C:\Users\SAKTHIVEL\Downloads\19.09.2024_15.30.16_636_7-removebg.cur")  # Replace with your cursor path
            
            voice_text = recognize_speech()
            response_text = backend.generate_response(voice_text)  # Get response from backend
            app.show(voice_text, response_text)  # Show both prompt and response

        elif key == keyboard.Key.esc:
            app.hide()  # Hide the box when Esc is pressed
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

# Main program
if __name__ == "__main__":    
    app = VoiceInputApp()

    # Start global hotkey listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        app.root.mainloop()  # Run the tkinter event loop
        listener.join()