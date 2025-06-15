import torch
import openai
import transformers
import speech_recognition as sr
import pyttsx3
import time
import os
import random
import sqlite

class AI_pipeline():

# === Initialize Speech Engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Change to [1] for female

def speak(text):
    print(f"Aalex: {text}")
    engine.say(text)
    engine.runAndWait()

# === Listen to Voice Commands ===
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("I didn't catch that.")
    except sr.RequestError:
        speak("Connection issue.")
    return ""

# === Simulated Suit Diagnostics ===
def run_diagnostics():
    status = {
        "Power Core": "96%",
        "Servo Motors": "All functioning",
        "HUD": "Operational",
        "Shield Tracker": "Connected",
        "Legs": "Calibrated",
    }
    speak("Running suit diagnostics.")
    for part, stat in status.items():
        speak(f"{part}: {stat}")
        time.sleep(0.5)

# === Commands Handler ===
def execute_command(cmd):
    if "diagnostics" in cmd:
        run_diagnostics()

    elif "recall shield" in cmd:
        speak("Recalling shield. Locking onto tracker signal.")
        time.sleep(1)
        speak("Shield returning to arm.")

    elif "activate stealth" in cmd:
        speak("Stealth mode engaged. Cloaking systems on standby.")

    elif "play music" in cmd:
        speak("Playing battle playlist.")
        os.system("start https://www.youtube.com/watch?v=QH2-TGUlwu4")  # change to your file or link

    elif "shutdown" in cmd:
        speak("Powering down. Stay safe.")
        exit()

    elif "hello" in cmd or "hi" in cmd:
        speak(random.choice(["Hello hero.", "At your service.", "System online and ready."]))

    elif "help" in cmd:
        speak("You can say: run diagnostics, recall shield, activate stealth, play music, or shutdown.")

    else:
        speak("Unknown command. Try again.")

# === MAIN LOOP ===
if __name__ == "__main__":
    speak("Aalex online. Welcome back.")
    while True:
        command = listen()
        if command:
            execute_command(command)
  





