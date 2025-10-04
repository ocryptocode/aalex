#!/usr/bin/env python3
"""
AALEX - AI Assistant Like Jarvis
A comprehensive AI assistant for Windows PC with voice recognition, TTS, and system control
"""

import speech_recognition as sr
import pyttsx3
import pyautogui
import psutil
import os
import subprocess
import webbrowser
import requests
import json
import time
import threading
from datetime import datetime
import win32api
import win32con
import win32gui
import ctypes
from ctypes import wintypes
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import scrolledtext

class AALEX:
    def __init__(self):
        """Initialize the AI assistant"""
        self.name = "AALEX"
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Configure TTS
        self.setup_tts()
        
        # Wake words
        self.wake_words = ["aalex", "alex", "hey aalex", "jarvis"]
        
        # Load custom commands
        self.load_custom_commands()
        
        # Commands mapping
        self.commands = {
            "time": self.get_time,
            "date": self.get_date,
            "weather": self.get_weather,
            "search": self.web_search,
            "open": self.open_application,
            "close": self.close_application,
            "volume": self.control_volume,
            "brightness": self.control_brightness,
            "screenshot": self.take_screenshot,
            "shutdown": self.shutdown_computer,
            "restart": self.restart_computer,
            "sleep": self.sleep_computer,
            "system": self.get_system_info,
            "battery": self.get_battery_info,
            "joke": self.tell_joke,
            "quote": self.tell_quote,
            "help": self.show_help,
            "control": self.open_control_pad,
            "settings": self.open_control_pad
        }
        
        # Merge custom commands
        self.commands.update(self.custom_commands)
        
        # Control pad window
        self.control_pad = None
        
        print(f"{self.name} initialized successfully!")
        self.speak("Hello! I'm AALEX, your AI assistant. Say 'control' to open the command hub!")
    
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.engine.getProperty('voices')
        # Try to find a male voice (more like Jarvis)
        for voice in voices:
            if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen for voice commands"""
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                print(f"Could not request results: {e}")
                return None
        except sr.WaitTimeoutError:
            return None
    
    def is_wake_word(self, text):
        """Check if the text contains a wake word"""
        if not text:
            return False
        return any(wake_word in text for wake_word in self.wake_words)
    
    def process_command(self, text):
        """Process the voice command"""
        if not text:
            return
        
        # Remove wake words from the command
        for wake_word in self.wake_words:
            text = text.replace(wake_word, "").strip()
        
        # Find matching command
        for command, function in self.commands.items():
            if command in text:
                try:
                    function(text)
                    return
                except Exception as e:
                    self.speak(f"Sorry, I encountered an error: {str(e)}")
                    return
        
        # If no specific command found, try to help
        self.speak("I didn't understand that command. Say 'help' to see available commands.")
    
    def get_time(self, text=""):
        """Get current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
    
    def get_date(self, text=""):
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        self.speak(f"Today is {current_date}")
    
    def get_weather(self, text=""):
        """Get weather information (requires API key)"""
        self.speak("Weather information requires an API key. Please configure your weather API key in the settings.")
    
    def web_search(self, text):
        """Perform web search"""
        query = text.replace("search", "").strip()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            self.speak(f"Searching for {query}")
        else:
            self.speak("What would you like me to search for?")
    
    def open_application(self, text):
        """Open applications"""
        app_name = text.replace("open", "").strip()
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "spotify": "spotify.exe",
            "discord": "discord.exe",
            "steam": "steam.exe"
        }
        
        if app_name in apps:
            try:
                subprocess.Popen(apps[app_name])
                self.speak(f"Opening {app_name}")
            except Exception as e:
                self.speak(f"Could not open {app_name}")
        else:
            self.speak(f"I don't know how to open {app_name}")
    
    def close_application(self, text):
        """Close applications"""
        app_name = text.replace("close", "").strip()
        self.speak(f"Closing {app_name}")
        # This is a simplified version - in practice, you'd need to find the specific process
    
    def control_volume(self, text):
        """Control system volume"""
        if "up" in text or "increase" in text:
            for _ in range(5):
                pyautogui.press('volumeup')
            self.speak("Volume increased")
        elif "down" in text or "decrease" in text:
            for _ in range(5):
                pyautogui.press('volumedown')
            self.speak("Volume decreased")
        elif "mute" in text:
            pyautogui.press('volumemute')
            self.speak("Volume muted")
        else:
            self.speak("Volume control: say 'volume up', 'volume down', or 'mute'")
    
    def control_brightness(self, text):
        """Control screen brightness"""
        if "up" in text or "increase" in text:
            self.speak("Brightness increased")
        elif "down" in text or "decrease" in text:
            self.speak("Brightness decreased")
        else:
            self.speak("Brightness control: say 'brightness up' or 'brightness down'")
    
    def take_screenshot(self, text=""):
        """Take a screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        self.speak("Screenshot taken and saved")
    
    def shutdown_computer(self, text=""):
        """Shutdown the computer"""
        self.speak("Shutting down the computer in 10 seconds. Say 'cancel' to abort.")
        time.sleep(10)
        os.system("shutdown /s /t 0")
    
    def restart_computer(self, text=""):
        """Restart the computer"""
        self.speak("Restarting the computer in 10 seconds. Say 'cancel' to abort.")
        time.sleep(10)
        os.system("shutdown /r /t 0")
    
    def sleep_computer(self, text=""):
        """Put computer to sleep"""
        self.speak("Putting computer to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    def get_system_info(self, text=""):
        """Get system information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"CPU usage: {cpu_percent}%, Memory usage: {memory.percent}%, Disk usage: {disk.percent}%"
        self.speak(info)
    
    def get_battery_info(self, text=""):
        """Get battery information"""
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            self.speak(f"Battery is at {percent}% and {plugged}")
        else:
            self.speak("No battery information available")
    
    def tell_joke(self, text=""):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    
    def tell_quote(self, text=""):
        """Tell an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle"
        ]
        quote = random.choice(quotes)
        self.speak(quote)
    
    def show_help(self, text=""):
        """Show available commands"""
        help_text = """
        Available commands:
        - Time: Get current time
        - Date: Get current date
        - Search: Search the web
        - Open: Open applications
        - Volume: Control volume
        - Screenshot: Take a screenshot
        - System: Get system information
        - Battery: Get battery information
        - Joke: Tell a joke
        - Quote: Tell an inspirational quote
        - Shutdown: Shutdown computer
        - Restart: Restart computer
        - Sleep: Put computer to sleep
        - Control: Open command control pad
        - Settings: Open command control pad
        """
        self.speak("Here are the available commands")
        print(help_text)
    
    def load_custom_commands(self):
        """Load custom commands from file"""
        self.custom_commands = {}
        try:
            if os.path.exists("aalex_custom_commands.json"):
                with open("aalex_custom_commands.json", 'r') as f:
                    data = json.load(f)
                    for command_name, command_data in data.items():
                        self.custom_commands[command_name] = self.create_custom_function(
                            command_data['action'], command_data['response']
                        )
        except Exception as e:
            print(f"Error loading custom commands: {e}")
            self.custom_commands = {}
    
    def save_custom_commands(self):
        """Save custom commands to file"""
        try:
            data = {}
            for command_name, command_func in self.custom_commands.items():
                # This is a simplified approach - in practice you'd store the command data
                data[command_name] = {
                    'action': 'custom',
                    'response': f'Executing custom command: {command_name}'
                }
            with open("aalex_custom_commands.json", 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving custom commands: {e}")
    
    def create_custom_function(self, action, response):
        """Create a custom function for a command"""
        def custom_func(text=""):
            self.speak(response)
            # Here you could add more complex actions based on the action type
        return custom_func
    
    def open_control_pad(self, text=""):
        """Open the command control pad"""
        if self.control_pad is None or not self.control_pad.winfo_exists():
            self.control_pad = AALEXControlPad(self)
        else:
            self.control_pad.lift()
        self.speak("Opening command control pad")
    
    def run(self):
        """Main loop for the AI assistant"""
        self.speak("AALEX is now active. Say my name to wake me up!")
        
        while True:
            try:
                # Listen for wake word
                text = self.listen()
                
                if text and self.is_wake_word(text):
                    self.speak("Yes, how can I help you?")
                    
                    # Listen for command
                    command = self.listen()
                    if command:
                        self.process_command(command)
                
                time.sleep(0.1)  # Small delay to prevent high CPU usage
                
            except KeyboardInterrupt:
                self.speak("Goodbye! AALEX is shutting down.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)

class AALEXControlPad:
    def __init__(self, aalex_instance):
        """Initialize the control pad"""
        self.aalex = aalex_instance
        self.root = tk.Tk()
        self.root.title("AALEX Command Control Pad")
        self.root.geometry("800x600")
        self.root.configure(bg='#0a0a0a')
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        # Center the window
        self.center_window()
        
        self.create_interface()
        
        # Load existing commands
        self.refresh_command_list()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_interface(self):
        """Create the control pad interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="AALEX Command Control Pad", 
                              font=('Arial', 18, 'bold'), fg='#00ff00', bg='#0a0a0a')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a1a')
        style.configure('TNotebook.Tab', background='#2a2a2a', foreground='#00ff00')
        
        # Create tabs
        self.create_commands_tab()
        self.create_custom_tab()
        self.create_settings_tab()
        self.create_test_tab()
    
    def create_commands_tab(self):
        """Create commands management tab"""
        commands_frame = ttk.Frame(self.notebook)
        self.notebook.add(commands_frame, text="🎯 Commands")
        
        # Commands interface
        commands_interface_frame = tk.Frame(commands_frame, bg='#1a1a1a')
        commands_interface_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(commands_interface_frame, text="Command Management", 
                font=('Arial', 14, 'bold'), fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 10))
        
        # Commands list
        list_frame = tk.Frame(commands_interface_frame, bg='#1a1a1a')
        list_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(list_frame, text="Available Commands", font=('Arial', 12, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        
        # Commands listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg='#1a1a1a')
        listbox_frame.pack(fill='both', expand=True)
        
        self.commands_listbox = tk.Listbox(listbox_frame, bg='#2a2a2a', fg='#ffffff', 
                                          selectbackground='#00ff00', height=15)
        self.commands_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        
        self.commands_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.commands_listbox.yview)
        
        # Command details
        details_frame = tk.Frame(commands_interface_frame, bg='#1a1a1a')
        details_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(details_frame, text="Command Details", font=('Arial', 12, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        
        self.command_details = scrolledtext.ScrolledText(details_frame, bg='#2a2a2a', 
                                                        fg='#ffffff', height=8, font=('Arial', 9))
        self.command_details.pack(fill='x')
        
        # Command actions
        actions_frame = tk.Frame(commands_interface_frame, bg='#1a1a1a')
        actions_frame.pack(fill='x')
        
        tk.Button(actions_frame, text="Test Command", bg='#00ff00', fg='#000000',
                 command=self.test_selected_command).pack(side='left', padx=(0, 5))
        tk.Button(actions_frame, text="Refresh List", bg='#0066ff', fg='#ffffff',
                 command=self.refresh_command_list).pack(side='left', padx=(0, 5))
        tk.Button(actions_frame, text="Export Commands", bg='#ff8800', fg='#ffffff',
                 command=self.export_commands).pack(side='left')
        
        # Bind selection event
        self.commands_listbox.bind('<<ListboxSelect>>', self.on_command_select)
    
    def create_custom_tab(self):
        """Create custom commands tab"""
        custom_frame = ttk.Frame(self.notebook)
        self.notebook.add(custom_frame, text="➕ Custom")
        
        # Custom commands interface
        custom_interface_frame = tk.Frame(custom_frame, bg='#1a1a1a')
        custom_interface_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(custom_interface_frame, text="Custom Commands", 
                font=('Arial', 14, 'bold'), fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 10))
        
        # Add new command form
        form_frame = tk.Frame(custom_interface_frame, bg='#2a2a2a', relief='raised', bd=2)
        form_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(form_frame, text="Add New Custom Command", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#2a2a2a').pack(pady=10)
        
        # Command name
        name_frame = tk.Frame(form_frame, bg='#2a2a2a')
        name_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(name_frame, text="Command Name:", fg='#ffffff', bg='#2a2a2a').pack(side='left')
        self.new_command_name = tk.Entry(name_frame, bg='#1a1a1a', fg='#ffffff', 
                                        insertbackground='#ffffff')
        self.new_command_name.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Command trigger words
        trigger_frame = tk.Frame(form_frame, bg='#2a2a2a')
        trigger_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(trigger_frame, text="Trigger Words:", fg='#ffffff', bg='#2a2a2a').pack(side='left')
        self.new_command_trigger = tk.Entry(trigger_frame, bg='#1a1a1a', fg='#ffffff', 
                                           insertbackground='#ffffff')
        self.new_command_trigger.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Command response
        response_frame = tk.Frame(form_frame, bg='#2a2a2a')
        response_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(response_frame, text="Response:", fg='#ffffff', bg='#2a2a2a').pack(anchor='w')
        self.new_command_response = tk.Text(response_frame, bg='#1a1a1a', fg='#ffffff', 
                                           insertbackground='#ffffff', height=3)
        self.new_command_response.pack(fill='x', pady=(5, 0))
        
        # Command action type
        action_frame = tk.Frame(form_frame, bg='#2a2a2a')
        action_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(action_frame, text="Action Type:", fg='#ffffff', bg='#2a2a2a').pack(side='left')
        self.new_command_action = ttk.Combobox(action_frame, values=[
            'speak', 'open_app', 'web_search', 'system_command', 'custom_script'
        ], state='readonly')
        self.new_command_action.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.new_command_action.set('speak')
        
        # Add command button
        tk.Button(form_frame, text="Add Custom Command", bg='#00ff00', fg='#000000',
                 command=self.add_custom_command).pack(pady=10)
        
        # Custom commands list
        custom_list_frame = tk.Frame(custom_interface_frame, bg='#1a1a1a')
        custom_list_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        tk.Label(custom_list_frame, text="Custom Commands", font=('Arial', 12, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        
        self.custom_commands_listbox = tk.Listbox(custom_list_frame, bg='#2a2a2a', fg='#ffffff', 
                                                 selectbackground='#00ff00', height=10)
        self.custom_commands_listbox.pack(fill='both', expand=True, pady=(0, 5))
        
        # Custom commands actions
        custom_actions_frame = tk.Frame(custom_list_frame, bg='#1a1a1a')
        custom_actions_frame.pack(fill='x')
        
        tk.Button(custom_actions_frame, text="Test", bg='#00ff00', fg='#000000',
                 command=self.test_custom_command).pack(side='left', padx=(0, 5))
        tk.Button(custom_actions_frame, text="Edit", bg='#0066ff', fg='#ffffff',
                 command=self.edit_custom_command).pack(side='left', padx=(0, 5))
        tk.Button(custom_actions_frame, text="Delete", bg='#ff4444', fg='#ffffff',
                 command=self.delete_custom_command).pack(side='left', padx=(0, 5))
        tk.Button(custom_actions_frame, text="Save All", bg='#ff8800', fg='#ffffff',
                 command=self.save_custom_commands).pack(side='right')
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings interface
        settings_interface_frame = tk.Frame(settings_frame, bg='#1a1a1a')
        settings_interface_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(settings_interface_frame, text="AALEX Settings", 
                font=('Arial', 14, 'bold'), fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 10))
        
        # Voice settings
        voice_frame = tk.Frame(settings_interface_frame, bg='#2a2a2a', relief='raised', bd=2)
        voice_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(voice_frame, text="Voice Settings", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#2a2a2a').pack(pady=10)
        
        # Speech rate
        rate_frame = tk.Frame(voice_frame, bg='#2a2a2a')
        rate_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(rate_frame, text="Speech Rate:", fg='#ffffff', bg='#2a2a2a').pack(side='left')
        self.speech_rate = tk.Scale(rate_frame, from_=100, to=300, orient='horizontal', 
                                   bg='#2a2a2a', fg='#ffffff')
        self.speech_rate.set(180)
        self.speech_rate.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Volume
        volume_frame = tk.Frame(voice_frame, bg='#2a2a2a')
        volume_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(volume_frame, text="Volume:", fg='#ffffff', bg='#2a2a2a').pack(side='left')
        self.volume = tk.Scale(volume_frame, from_=0.0, to=1.0, resolution=0.1, 
                              orient='horizontal', bg='#2a2a2a', fg='#ffffff')
        self.volume.set(0.9)
        self.volume.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Wake words settings
        wake_frame = tk.Frame(settings_interface_frame, bg='#2a2a2a', relief='raised', bd=2)
        wake_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(wake_frame, text="Wake Words", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#2a2a2a').pack(pady=10)
        
        wake_words_frame = tk.Frame(wake_frame, bg='#2a2a2a')
        wake_words_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(wake_words_frame, text="Wake Words (comma separated):", 
                fg='#ffffff', bg='#2a2a2a').pack(anchor='w')
        self.wake_words_entry = tk.Entry(wake_words_frame, bg='#1a1a1a', fg='#ffffff', 
                                        insertbackground='#ffffff')
        self.wake_words_entry.pack(fill='x', pady=(5, 0))
        self.wake_words_entry.insert(0, ', '.join(self.aalex.wake_words))
        
        # Apply settings button
        tk.Button(settings_interface_frame, text="Apply Settings", bg='#00ff00', fg='#000000',
                 command=self.apply_settings).pack(pady=10)
    
    def create_test_tab(self):
        """Create test tab"""
        test_frame = ttk.Frame(self.notebook)
        self.notebook.add(test_frame, text="🧪 Test")
        
        # Test interface
        test_interface_frame = tk.Frame(test_frame, bg='#1a1a1a')
        test_interface_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(test_interface_frame, text="Command Testing", 
                font=('Arial', 14, 'bold'), fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 10))
        
        # Test input
        test_input_frame = tk.Frame(test_interface_frame, bg='#1a1a1a')
        test_input_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(test_input_frame, text="Test Command:", fg='#ffffff', bg='#1a1a1a').pack(anchor='w')
        self.test_command_entry = tk.Entry(test_input_frame, bg='#2a2a2a', fg='#ffffff', 
                                          insertbackground='#ffffff')
        self.test_command_entry.pack(fill='x', pady=(5, 0))
        self.test_command_entry.bind('<Return>', self.test_command)
        
        # Test button
        tk.Button(test_input_frame, text="Test Command", bg='#00ff00', fg='#000000',
                 command=self.test_command).pack(pady=(5, 0))
        
        # Test results
        results_frame = tk.Frame(test_interface_frame, bg='#1a1a1a')
        results_frame.pack(fill='both', expand=True)
        
        tk.Label(results_frame, text="Test Results", font=('Arial', 12, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        
        self.test_results = scrolledtext.ScrolledText(results_frame, bg='#2a2a2a', 
                                                     fg='#ffffff', height=15, font=('Consolas', 9))
        self.test_results.pack(fill='both', expand=True)
        
        # Test actions
        test_actions_frame = tk.Frame(test_interface_frame, bg='#1a1a1a')
        test_actions_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(test_actions_frame, text="Clear Results", bg='#ff4444', fg='#ffffff',
                 command=self.clear_test_results).pack(side='left', padx=(0, 5))
        tk.Button(test_actions_frame, text="Test All Commands", bg='#0066ff', fg='#ffffff',
                 command=self.test_all_commands).pack(side='left')
    
    def refresh_command_list(self):
        """Refresh the commands list"""
        self.commands_listbox.delete(0, tk.END)
        for command_name in self.aalex.commands.keys():
            self.commands_listbox.insert(tk.END, command_name)
    
    def on_command_select(self, event):
        """Handle command selection"""
        selection = self.commands_listbox.curselection()
        if selection:
            command_name = self.commands_listbox.get(selection[0])
            self.command_details.delete("1.0", tk.END)
            
            # Get command function
            command_func = self.aalex.commands.get(command_name)
            if command_func:
                details = f"Command: {command_name}\n"
                details += f"Function: {command_func.__name__}\n"
                details += f"Module: {command_func.__module__}\n"
                details += f"Docstring: {command_func.__doc__ or 'No documentation'}\n"
                self.command_details.insert(tk.END, details)
    
    def test_selected_command(self):
        """Test the selected command"""
        selection = self.commands_listbox.curselection()
        if selection:
            command_name = self.commands_listbox.get(selection[0])
            self.test_results.insert(tk.END, f"Testing command: {command_name}\n")
            try:
                command_func = self.aalex.commands.get(command_name)
                if command_func:
                    command_func("test")
                    self.test_results.insert(tk.END, f"✓ Command '{command_name}' executed successfully\n")
                else:
                    self.test_results.insert(tk.END, f"✗ Command '{command_name}' not found\n")
            except Exception as e:
                self.test_results.insert(tk.END, f"✗ Error testing '{command_name}': {str(e)}\n")
            self.test_results.see(tk.END)
    
    def test_command(self, event=None):
        """Test a command from the test tab"""
        command_text = self.test_command_entry.get().strip()
        if command_text:
            self.test_results.insert(tk.END, f"Testing: '{command_text}'\n")
            try:
                self.aalex.process_command(command_text)
                self.test_results.insert(tk.END, f"✓ Command processed successfully\n")
            except Exception as e:
                self.test_results.insert(tk.END, f"✗ Error: {str(e)}\n")
            self.test_results.see(tk.END)
            self.test_command_entry.delete(0, tk.END)
    
    def test_all_commands(self):
        """Test all available commands"""
        self.test_results.insert(tk.END, "Testing all commands...\n")
        for command_name in self.aalex.commands.keys():
            try:
                command_func = self.aalex.commands.get(command_name)
                if command_func:
                    command_func("test")
                    self.test_results.insert(tk.END, f"✓ {command_name}\n")
                else:
                    self.test_results.insert(tk.END, f"✗ {command_name} (not found)\n")
            except Exception as e:
                self.test_results.insert(tk.END, f"✗ {command_name} (error: {str(e)})\n")
        self.test_results.see(tk.END)
    
    def clear_test_results(self):
        """Clear test results"""
        self.test_results.delete("1.0", tk.END)
    
    def add_custom_command(self):
        """Add a new custom command"""
        name = self.new_command_name.get().strip()
        trigger = self.new_command_trigger.get().strip()
        response = self.new_command_response.get("1.0", tk.END).strip()
        action = self.new_command_action.get()
        
        if name and trigger and response:
            # Add to custom commands
            self.aalex.custom_commands[name] = self.aalex.create_custom_function(action, response)
            
            # Clear form
            self.new_command_name.delete(0, tk.END)
            self.new_command_trigger.delete(0, tk.END)
            self.new_command_response.delete("1.0", tk.END)
            
            # Refresh lists
            self.refresh_command_list()
            self.refresh_custom_commands_list()
            
            messagebox.showinfo("Success", f"Custom command '{name}' added successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields!")
    
    def refresh_custom_commands_list(self):
        """Refresh custom commands list"""
        self.custom_commands_listbox.delete(0, tk.END)
        for command_name in self.aalex.custom_commands.keys():
            self.custom_commands_listbox.insert(tk.END, command_name)
    
    def test_custom_command(self):
        """Test selected custom command"""
        selection = self.custom_commands_listbox.curselection()
        if selection:
            command_name = self.custom_commands_listbox.get(selection[0])
            try:
                command_func = self.aalex.custom_commands.get(command_name)
                if command_func:
                    command_func("test")
                    messagebox.showinfo("Test", f"Custom command '{command_name}' executed!")
            except Exception as e:
                messagebox.showerror("Error", f"Error testing command: {str(e)}")
    
    def edit_custom_command(self):
        """Edit selected custom command"""
        selection = self.custom_commands_listbox.curselection()
        if selection:
            command_name = self.custom_commands_listbox.get(selection[0])
            messagebox.showinfo("Edit", f"Edit functionality for '{command_name}' - Coming soon!")
    
    def delete_custom_command(self):
        """Delete selected custom command"""
        selection = self.custom_commands_listbox.curselection()
        if selection:
            command_name = self.custom_commands_listbox.get(selection[0])
            if messagebox.askyesno("Confirm", f"Delete custom command '{command_name}'?"):
                del self.aalex.custom_commands[command_name]
                self.refresh_command_list()
                self.refresh_custom_commands_list()
    
    def save_custom_commands(self):
        """Save custom commands"""
        self.aalex.save_custom_commands()
        messagebox.showinfo("Success", "Custom commands saved!")
    
    def apply_settings(self):
        """Apply settings"""
        # Update speech rate and volume
        self.aalex.engine.setProperty('rate', self.speech_rate.get())
        self.aalex.engine.setProperty('volume', self.volume.get())
        
        # Update wake words
        wake_words_text = self.wake_words_entry.get().strip()
        if wake_words_text:
            self.aalex.wake_words = [w.strip() for w in wake_words_text.split(',')]
        
        messagebox.showinfo("Success", "Settings applied successfully!")
    
    def export_commands(self):
        """Export commands to file"""
        try:
            commands_data = {
                'built_in_commands': list(self.aalex.commands.keys()),
                'custom_commands': list(self.aalex.custom_commands.keys()),
                'wake_words': self.aalex.wake_words
            }
            
            filename = f"aalex_commands_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(commands_data, f, indent=2)
            
            messagebox.showinfo("Export", f"Commands exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def run(self):
        """Run the control pad"""
        self.root.mainloop()

def main():
    """Main function to run AALEX"""
    print("Starting AALEX - AI Assistant Like Jarvis")
    print("=" * 50)
    
    try:
        aalex = AALEX()
        aalex.run()
    except Exception as e:
        print(f"Failed to start AALEX: {e}")
        print("Make sure you have all required dependencies installed.")

if __name__ == "__main__":
    main()
