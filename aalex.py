# import modules and libraries
import speech_recognition as sr
import pyttsx3
import time
import os
import random
import requests
import sqlite   

# === Initialize Speech Engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('voice', engine.getProperty('voices')[0].id)  

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

# === system ===



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

function aalex_brain(user_input):
    memory = get_memory()
    context = fetch_recent_chats()
    
    prompt = format_prompt(user_input, memory, context)
    response = LLM.generate(prompt)
    
    command = parse_response(response)
    if command:
        result = execute_command(command)
        update_memory(result)
    
    return result or response

function get_memory():
    return {
        "name": "Oussama",
        "projects": ["VORTEX", "PPH", "Crypto Tracker"],
        "roles": ["Founder", "Dev", "Marketer"],
        "preferences": ["Fast replies", "Crypto-friendly", "Build > Talk"]
    }

function fetch_recent_chats():
    return vector_search("last 5 relevant convos")

function update_memory(new_data):
    append_to_vector_db(new_data)
    update_structured_profile(new_data)

function parse_response(response):
    if response contains "command:":
        return extract_json_command(response)
    else:
        return None

function execute_command(command):
    if command["command"] == "tweet":
        return XAgent.post_tweet(command["content"])
    elif command["command"] == "update_readme":
        return CodeAgent.push_to_repo(command["repo"], command["text"])
    elif command["command"] == "email_user":
        return EmailAgent.send(command["to"], command["subject"], command["body"])
    else:
        return "Unknown command"


class CodeAgent:
    def push_to_repo(repo, text):
        # Use GitHub API or local Git
        commit(text)
        push(repo)
        return "Code pushed to " + repo

while True:
    user_input = listen_to_user()  # Text, speech, or UI
    response = aalex_brain(user_input)
    print("Aalex:", response)


# == extracting chatgpt data == # using pinecone
def extract_data():
    data = openai.


    return get_memory()



# running browser agent
class nexus_browser(self, data):
    self.data = 


# running tech setup (how ? => have aalex manage through arduinos)
class AI_pipeline(self, model ....):
    self.model = 
    
     # integrate ai models
# 
