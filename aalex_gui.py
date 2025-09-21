#!/usr/bin/env python3
"""
AALEX GUI - Advanced AI Assistant with Iron Man-like Interface
Features: Notes system, code snippets, screen analysis, ChatGPT integration, social media management
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import json
import os
from datetime import datetime
import requests
import webbrowser
from PIL import Image, ImageTk
import pyautogui
import psutil
import win32gui
import win32con
import win32api
from aalex import AALEX

class AALEXGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AALEX - AI Assistant")
        self.root.geometry("400x600")
        self.root.configure(bg='#0a0a0a')
        
        # Make window always on top and transparent
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        
        # Position in top-left corner
        self.root.geometry("+10+10")
        
        # Initialize components
        self.notes_data = []
        self.code_snippets = []
        self.social_tabs = {}
        self.chatgpt_api_key = ""
        self.is_monitoring = False
        
        # Load saved data
        self.load_data()
        
        # Create GUI
        self.create_gui()
        
        # Start monitoring thread
        self.start_monitoring()
    
    def create_gui(self):
        """Create the main GUI interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="AALEX", font=('Arial', 16, 'bold'), 
                              fg='#00ff00', bg='#0a0a0a')
        title_label.pack(pady=(0, 10))
        
        # Status indicator
        self.status_label = tk.Label(main_frame, text="● ACTIVE", font=('Arial', 10), 
                                    fg='#00ff00', bg='#0a0a0a')
        self.status_label.pack(pady=(0, 10))
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a1a')
        style.configure('TNotebook.Tab', background='#2a2a2a', foreground='#00ff00')
        
        # Create tabs
        self.create_notes_tab()
        self.create_code_tab()
        self.create_analysis_tab()
        self.create_chatgpt_tab()
        self.create_social_tab()
        self.create_settings_tab()
    
    def create_notes_tab(self):
        """Create notes tab"""
        notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(notes_frame, text="📝 Notes")
        
        # Notes list
        notes_list_frame = tk.Frame(notes_frame, bg='#1a1a1a')
        notes_list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(notes_list_frame, text="Quick Notes", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 5))
        
        # Notes listbox
        self.notes_listbox = tk.Listbox(notes_list_frame, bg='#2a2a2a', fg='#ffffff', 
                                       selectbackground='#00ff00', height=8)
        self.notes_listbox.pack(fill='both', expand=True, pady=(0, 5))
        
        # Add note entry
        note_entry_frame = tk.Frame(notes_list_frame, bg='#1a1a1a')
        note_entry_frame.pack(fill='x', pady=(0, 5))
        
        self.note_entry = tk.Entry(note_entry_frame, bg='#2a2a2a', fg='#ffffff', 
                                  insertbackground='#ffffff')
        self.note_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.note_entry.bind('<Return>', self.add_note)
        
        add_note_btn = tk.Button(note_entry_frame, text="+", bg='#00ff00', fg='#000000',
                                command=self.add_note, width=3)
        add_note_btn.pack(side='right')
        
        # Note actions
        note_actions_frame = tk.Frame(notes_list_frame, bg='#1a1a1a')
        note_actions_frame.pack(fill='x')
        
        tk.Button(note_actions_frame, text="Delete", bg='#ff4444', fg='#ffffff',
                 command=self.delete_note).pack(side='left', padx=(0, 5))
        tk.Button(note_actions_frame, text="Clear All", bg='#ff4444', fg='#ffffff',
                 command=self.clear_notes).pack(side='left')
        
        # Load existing notes
        self.refresh_notes()
    
    def create_code_tab(self):
        """Create code snippets tab"""
        code_frame = ttk.Frame(self.notebook)
        self.notebook.add(code_frame, text="💻 Code")
        
        # Code snippets list
        code_list_frame = tk.Frame(code_frame, bg='#1a1a1a')
        code_list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(code_list_frame, text="Code Snippets", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 5))
        
        # Code listbox
        self.code_listbox = tk.Listbox(code_list_frame, bg='#2a2a2a', fg='#ffffff', 
                                      selectbackground='#00ff00', height=6)
        self.code_listbox.pack(fill='both', expand=True, pady=(0, 5))
        
        # Code editor
        self.code_editor = scrolledtext.ScrolledText(code_list_frame, bg='#2a2a2a', 
                                                    fg='#ffffff', height=8, font=('Consolas', 10))
        self.code_editor.pack(fill='both', expand=True, pady=(0, 5))
        
        # Code actions
        code_actions_frame = tk.Frame(code_list_frame, bg='#1a1a1a')
        code_actions_frame.pack(fill='x')
        
        tk.Button(code_actions_frame, text="Save", bg='#00ff00', fg='#000000',
                 command=self.save_code_snippet).pack(side='left', padx=(0, 5))
        tk.Button(code_actions_frame, text="Copy", bg='#0066ff', fg='#ffffff',
                 command=self.copy_code).pack(side='left', padx=(0, 5))
        tk.Button(code_actions_frame, text="Delete", bg='#ff4444', fg='#ffffff',
                 command=self.delete_code_snippet).pack(side='left')
        
        # Load existing code snippets
        self.refresh_code_snippets()
    
    def create_analysis_tab(self):
        """Create screen analysis tab"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="🔍 Analysis")
        
        # Analysis display
        analysis_display_frame = tk.Frame(analysis_frame, bg='#1a1a1a')
        analysis_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(analysis_display_frame, text="Screen Analysis", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 5))
        
        # Analysis text
        self.analysis_text = scrolledtext.ScrolledText(analysis_display_frame, bg='#2a2a2a', 
                                                      fg='#ffffff', height=15, font=('Arial', 9))
        self.analysis_text.pack(fill='both', expand=True, pady=(0, 5))
        
        # Analysis controls
        analysis_controls_frame = tk.Frame(analysis_display_frame, bg='#1a1a1a')
        analysis_controls_frame.pack(fill='x')
        
        tk.Button(analysis_controls_frame, text="Analyze Screen", bg='#00ff00', fg='#000000',
                 command=self.analyze_screen).pack(side='left', padx=(0, 5))
        tk.Button(analysis_controls_frame, text="Monitor Apps", bg='#0066ff', fg='#ffffff',
                 command=self.toggle_monitoring).pack(side='left', padx=(0, 5))
        tk.Button(analysis_controls_frame, text="Clear", bg='#ff4444', fg='#ffffff',
                 command=self.clear_analysis).pack(side='left')
    
    def create_chatgpt_tab(self):
        """Create ChatGPT integration tab"""
        chatgpt_frame = ttk.Frame(self.notebook)
        self.notebook.add(chatgpt_frame, text="🤖 ChatGPT")
        
        # ChatGPT interface
        chatgpt_interface_frame = tk.Frame(chatgpt_frame, bg='#1a1a1a')
        chatgpt_interface_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(chatgpt_interface_frame, text="ChatGPT Integration", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 5))
        
        # API key entry
        api_key_frame = tk.Frame(chatgpt_interface_frame, bg='#1a1a1a')
        api_key_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(api_key_frame, text="API Key:", fg='#ffffff', bg='#1a1a1a').pack(side='left')
        self.api_key_entry = tk.Entry(api_key_frame, bg='#2a2a2a', fg='#ffffff', 
                                     insertbackground='#ffffff', show='*')
        self.api_key_entry.pack(side='left', fill='x', expand=True, padx=(5, 5))
        self.api_key_entry.insert(0, self.chatgpt_api_key)
        
        tk.Button(api_key_frame, text="Save", bg='#00ff00', fg='#000000',
                 command=self.save_api_key).pack(side='right')
        
        # Chat interface
        self.chat_display = scrolledtext.ScrolledText(chatgpt_interface_frame, bg='#2a2a2a', 
                                                     fg='#ffffff', height=12, font=('Arial', 9))
        self.chat_display.pack(fill='both', expand=True, pady=(0, 5))
        
        # Chat input
        chat_input_frame = tk.Frame(chatgpt_interface_frame, bg='#1a1a1a')
        chat_input_frame.pack(fill='x', pady=(0, 5))
        
        self.chat_input = tk.Entry(chat_input_frame, bg='#2a2a2a', fg='#ffffff', 
                                  insertbackground='#ffffff')
        self.chat_input.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.chat_input.bind('<Return>', self.send_chatgpt_message)
        
        tk.Button(chat_input_frame, text="Send", bg='#00ff00', fg='#000000',
                 command=self.send_chatgpt_message).pack(side='right')
    
    def create_social_tab(self):
        """Create social media management tab"""
        social_frame = ttk.Frame(self.notebook)
        self.notebook.add(social_frame, text="📱 Social")
        
        # Social media interface
        social_interface_frame = tk.Frame(social_frame, bg='#1a1a1a')
        social_interface_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(social_interface_frame, text="Social Media Manager", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 5))
        
        # Social platform buttons
        social_buttons_frame = tk.Frame(social_interface_frame, bg='#1a1a1a')
        social_buttons_frame.pack(fill='x', pady=(0, 10))
        
        platforms = [
            ("Twitter", "https://twitter.com", "#1da1f2"),
            ("LinkedIn", "https://linkedin.com", "#0077b5"),
            ("Facebook", "https://facebook.com", "#4267b2"),
            ("Instagram", "https://instagram.com", "#e4405f"),
            ("YouTube", "https://youtube.com", "#ff0000"),
            ("Reddit", "https://reddit.com", "#ff4500")
        ]
        
        for i, (platform, url, color) in enumerate(platforms):
            btn = tk.Button(social_buttons_frame, text=platform, bg=color, fg='#ffffff',
                           command=lambda u=url: self.open_social_platform(u))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky='ew')
        
        # Configure grid weights
        for i in range(3):
            social_buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Social feed display
        self.social_display = scrolledtext.ScrolledText(social_interface_frame, bg='#2a2a2a', 
                                                       fg='#ffffff', height=15, font=('Arial', 9))
        self.social_display.pack(fill='both', expand=True, pady=(0, 5))
        
        # Social actions
        social_actions_frame = tk.Frame(social_interface_frame, bg='#1a1a1a')
        social_actions_frame.pack(fill='x')
        
        tk.Button(social_actions_frame, text="Refresh Feed", bg='#00ff00', fg='#000000',
                 command=self.refresh_social_feed).pack(side='left', padx=(0, 5))
        tk.Button(social_actions_frame, text="Open Browser", bg='#0066ff', fg='#ffffff',
                 command=self.open_aalex_browser).pack(side='left')
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings interface
        settings_interface_frame = tk.Frame(settings_frame, bg='#1a1a1a')
        settings_interface_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Label(settings_interface_frame, text="AALEX Settings", font=('Arial', 12, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=(0, 10))
        
        # Auto-save settings
        self.auto_save_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings_interface_frame, text="Auto-save data", variable=self.auto_save_var,
                      fg='#ffffff', bg='#1a1a1a', selectcolor='#2a2a2a').pack(anchor='w', pady=2)
        
        # Always on top
        self.always_on_top_var = tk.BooleanVar(value=True)
        tk.Checkbutton(settings_interface_frame, text="Always on top", variable=self.always_on_top_var,
                      fg='#ffffff', bg='#1a1a1a', selectcolor='#2a2a2a',
                      command=self.toggle_always_on_top).pack(anchor='w', pady=2)
        
        # Transparency
        transparency_frame = tk.Frame(settings_interface_frame, bg='#1a1a1a')
        transparency_frame.pack(fill='x', pady=10)
        
        tk.Label(transparency_frame, text="Transparency:", fg='#ffffff', bg='#1a1a1a').pack(side='left')
        self.transparency_scale = tk.Scale(transparency_frame, from_=0.5, to=1.0, resolution=0.1,
                                          orient='horizontal', bg='#2a2a2a', fg='#ffffff',
                                          command=self.update_transparency)
        self.transparency_scale.set(0.9)
        self.transparency_scale.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Data management
        data_frame = tk.Frame(settings_interface_frame, bg='#1a1a1a')
        data_frame.pack(fill='x', pady=10)
        
        tk.Label(data_frame, text="Data Management", font=('Arial', 10, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(anchor='w', pady=(0, 5))
        
        tk.Button(data_frame, text="Export Data", bg='#00ff00', fg='#000000',
                 command=self.export_data).pack(side='left', padx=(0, 5))
        tk.Button(data_frame, text="Import Data", bg='#0066ff', fg='#ffffff',
                 command=self.import_data).pack(side='left', padx=(0, 5))
        tk.Button(data_frame, text="Reset All", bg='#ff4444', fg='#ffffff',
                 command=self.reset_all_data).pack(side='left')
    
    def add_note(self, event=None):
        """Add a new note"""
        note_text = self.note_entry.get().strip()
        if note_text:
            timestamp = datetime.now().strftime("%H:%M")
            note = f"[{timestamp}] {note_text}"
            self.notes_data.append(note)
            self.note_entry.delete(0, tk.END)
            self.refresh_notes()
            self.save_data()
    
    def delete_note(self):
        """Delete selected note"""
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            del self.notes_data[index]
            self.refresh_notes()
            self.save_data()
    
    def clear_notes(self):
        """Clear all notes"""
        if messagebox.askyesno("Confirm", "Clear all notes?"):
            self.notes_data.clear()
            self.refresh_notes()
            self.save_data()
    
    def refresh_notes(self):
        """Refresh notes listbox"""
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes_data:
            self.notes_listbox.insert(tk.END, note)
    
    def save_code_snippet(self):
        """Save code snippet"""
        code_text = self.code_editor.get("1.0", tk.END).strip()
        if code_text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            snippet = {
                "timestamp": timestamp,
                "code": code_text
            }
            self.code_snippets.append(snippet)
            self.refresh_code_snippets()
            self.save_data()
    
    def copy_code(self):
        """Copy selected code to clipboard"""
        code_text = self.code_editor.get("1.0", tk.END).strip()
        if code_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(code_text)
            self.status_label.config(text="● Code copied to clipboard")
    
    def delete_code_snippet(self):
        """Delete selected code snippet"""
        selection = self.code_listbox.curselection()
        if selection:
            index = selection[0]
            del self.code_snippets[index]
            self.refresh_code_snippets()
            self.save_data()
    
    def refresh_code_snippets(self):
        """Refresh code snippets listbox"""
        self.code_listbox.delete(0, tk.END)
        for i, snippet in enumerate(self.code_snippets):
            self.code_listbox.insert(tk.END, f"{i+1}. {snippet['timestamp']}")
    
    def analyze_screen(self):
        """Analyze current screen content"""
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Get active window info
            active_window = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(active_window)
            
            # Get system info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Analyze running processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    if proc.info['cpu_percent'] > 1.0:
                        processes.append(f"{proc.info['name']}: {proc.info['cpu_percent']:.1f}%")
                except:
                    pass
            
            analysis = f"""
SCREEN ANALYSIS - {datetime.now().strftime("%H:%M:%S")}
{'='*50}
Active Window: {window_title}
CPU Usage: {cpu_percent}%
Memory Usage: {memory.percent}%
Available Memory: {memory.available // (1024**3)} GB

Top CPU Processes:
{chr(10).join(processes[:5])}

Screen Resolution: {screenshot.size}
Screenshot saved: screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png
"""
            
            self.analysis_text.insert(tk.END, analysis + "\n")
            self.analysis_text.see(tk.END)
            
            # Save screenshot
            screenshot.save(f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
        except Exception as e:
            self.analysis_text.insert(tk.END, f"Analysis error: {str(e)}\n")
    
    def toggle_monitoring(self):
        """Toggle application monitoring"""
        self.is_monitoring = not self.is_monitoring
        if self.is_monitoring:
            self.status_label.config(text="● MONITORING")
            self.start_monitoring_thread()
        else:
            self.status_label.config(text="● ACTIVE")
    
    def start_monitoring_thread(self):
        """Start monitoring thread"""
        def monitor():
            while self.is_monitoring:
                try:
                    # Get active window
                    active_window = win32gui.GetForegroundWindow()
                    window_title = win32gui.GetWindowText(active_window)
                    
                    # Log activity
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    activity = f"[{timestamp}] Using: {window_title}"
                    
                    self.analysis_text.insert(tk.END, activity + "\n")
                    self.analysis_text.see(tk.END)
                    
                    time.sleep(5)  # Monitor every 5 seconds
                except:
                    break
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def clear_analysis(self):
        """Clear analysis text"""
        self.analysis_text.delete("1.0", tk.END)
    
    def save_api_key(self):
        """Save ChatGPT API key"""
        self.chatgpt_api_key = self.api_key_entry.get().strip()
        self.save_data()
        self.chat_display.insert(tk.END, "API key saved!\n")
    
    def send_chatgpt_message(self, event=None):
        """Send message to ChatGPT"""
        message = self.chat_input.get().strip()
        if not message:
            return
        
        if not self.chatgpt_api_key:
            self.chat_display.insert(tk.END, "Please enter your ChatGPT API key first!\n")
            return
        
        # Display user message
        self.chat_display.insert(tk.END, f"You: {message}\n")
        self.chat_input.delete(0, tk.END)
        
        # Send to ChatGPT (simplified - you'd need to implement actual API call)
        self.chat_display.insert(tk.END, "ChatGPT: [API integration needed]\n")
        self.chat_display.see(tk.END)
    
    def open_social_platform(self, url):
        """Open social media platform"""
        webbrowser.open(url)
        self.social_display.insert(tk.END, f"Opened: {url}\n")
    
    def refresh_social_feed(self):
        """Refresh social media feed"""
        self.social_display.insert(tk.END, f"Refreshing social feed... {datetime.now().strftime('%H:%M:%S')}\n")
        # Here you would integrate with social media APIs
    
    def open_aalex_browser(self):
        """Open AALEX browser"""
        webbrowser.open("https://www.google.com")
        self.social_display.insert(tk.END, "AALEX Browser opened\n")
    
    def toggle_always_on_top(self):
        """Toggle always on top"""
        self.root.attributes('-topmost', self.always_on_top_var.get())
    
    def update_transparency(self, value):
        """Update window transparency"""
        self.root.attributes('-alpha', float(value))
    
    def export_data(self):
        """Export all data to JSON"""
        data = {
            "notes": self.notes_data,
            "code_snippets": self.code_snippets,
            "chatgpt_api_key": self.chatgpt_api_key
        }
        
        filename = f"aalex_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        messagebox.showinfo("Export", f"Data exported to {filename}")
    
    def import_data(self):
        """Import data from JSON"""
        # Simplified - you'd add file dialog here
        messagebox.showinfo("Import", "Import functionality - select JSON file")
    
    def reset_all_data(self):
        """Reset all data"""
        if messagebox.askyesno("Confirm", "Reset all data? This cannot be undone!"):
            self.notes_data.clear()
            self.code_snippets.clear()
            self.chatgpt_api_key = ""
            self.refresh_notes()
            self.refresh_code_snippets()
            self.save_data()
    
    def load_data(self):
        """Load saved data"""
        try:
            if os.path.exists("aalex_data.json"):
                with open("aalex_data.json", 'r') as f:
                    data = json.load(f)
                    self.notes_data = data.get("notes", [])
                    self.code_snippets = data.get("code_snippets", [])
                    self.chatgpt_api_key = data.get("chatgpt_api_key", "")
        except:
            pass
    
    def save_data(self):
        """Save data to file"""
        if self.auto_save_var.get():
            try:
                data = {
                    "notes": self.notes_data,
                    "code_snippets": self.code_snippets,
                    "chatgpt_api_key": self.chatgpt_api_key
                }
                with open("aalex_data.json", 'w') as f:
                    json.dump(data, f, indent=2)
            except:
                pass
    
    def start_monitoring(self):
        """Start initial monitoring"""
        def update_status():
            while True:
                try:
                    # Update status every 30 seconds
                    time.sleep(30)
                    if not self.is_monitoring:
                        self.status_label.config(text="● ACTIVE")
                except:
                    break
        
        thread = threading.Thread(target=update_status, daemon=True)
        thread.start()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting AALEX GUI...")
    app = AALEXGUI()
    app.run()

if __name__ == "__main__":
    main()
