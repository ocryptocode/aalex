#!/usr/bin/env python3
"""
AALEX Launcher - Main launcher for the complete AI assistant system
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import sys
from datetime import datetime

class AALEXLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AALEX - AI Assistant Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg='#0a0a0a')
        
        # Center the window
        self.center_window()
        
        # Initialize components
        self.processes = {}
        
        self.create_launcher_interface()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_launcher_interface(self):
        """Create the launcher interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="AALEX", font=('Arial', 24, 'bold'), 
                              fg='#00ff00', bg='#0a0a0a')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame, text="AI Assistant Like Jarvis", font=('Arial', 12), 
                                 fg='#ffffff', bg='#0a0a0a')
        subtitle_label.pack(pady=(0, 20))
        
        # Status
        self.status_label = tk.Label(main_frame, text="Ready to launch", font=('Arial', 10), 
                                    fg='#00ff00', bg='#0a0a0a')
        self.status_label.pack(pady=(0, 20))
        
        # Components frame
        components_frame = tk.Frame(main_frame, bg='#1a1a1a', relief='raised', bd=2)
        components_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        tk.Label(components_frame, text="AALEX Components", font=('Arial', 14, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=10)
        
        # Component buttons
        components = [
            ("🎤 Voice Assistant", "aalex.py", "Core voice recognition and system control"),
            ("🖥️ GUI Interface", "aalex_gui.py", "Iron Man-like overlay with notes and code snippets"),
            ("🌐 AALEX Browser", "aalex_browser.py", "Integrated browser for social media and AI tools"),
            ("🚀 Launch All", "all", "Start all AALEX components")
        ]
        
        for i, (name, script, description) in enumerate(components):
            component_frame = tk.Frame(components_frame, bg='#2a2a2a', relief='raised', bd=1)
            component_frame.pack(fill='x', padx=10, pady=5)
            
            # Component info
            info_frame = tk.Frame(component_frame, bg='#2a2a2a')
            info_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            
            tk.Label(info_frame, text=name, font=('Arial', 12, 'bold'), 
                    fg='#00ff00', bg='#2a2a2a').pack(anchor='w')
            tk.Label(info_frame, text=description, font=('Arial', 9), 
                    fg='#ffffff', bg='#2a2a2a').pack(anchor='w')
            
            # Launch button
            launch_btn = tk.Button(component_frame, text="Launch", bg='#00ff00', fg='#000000',
                                  font=('Arial', 10, 'bold'), width=10,
                                  command=lambda s=script: self.launch_component(s))
            launch_btn.pack(side='right', padx=10, pady=10)
        
        # Control buttons
        control_frame = tk.Frame(main_frame, bg='#0a0a0a')
        control_frame.pack(fill='x')
        
        tk.Button(control_frame, text="Stop All", bg='#ff4444', fg='#ffffff',
                 font=('Arial', 10, 'bold'), command=self.stop_all_components).pack(side='left', padx=(0, 10))
        
        tk.Button(control_frame, text="Check Status", bg='#0066ff', fg='#ffffff',
                 font=('Arial', 10, 'bold'), command=self.check_status).pack(side='left', padx=(0, 10))
        
        tk.Button(control_frame, text="Exit", bg='#666666', fg='#ffffff',
                 font=('Arial', 10, 'bold'), command=self.exit_launcher).pack(side='right')
        
        # Log display
        log_frame = tk.Frame(main_frame, bg='#1a1a1a', relief='raised', bd=2)
        log_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(log_frame, text="Launch Log", font=('Arial', 10, 'bold'), 
                fg='#00ff00', bg='#1a1a1a').pack(pady=5)
        
        self.log_text = tk.Text(log_frame, bg='#2a2a2a', fg='#ffffff', height=6, 
                               font=('Consolas', 9))
        self.log_text.pack(fill='x', padx=10, pady=(0, 10))
        
        # Initial log message
        self.log_message("AALEX Launcher initialized")
    
    def launch_component(self, script):
        """Launch a component"""
        try:
            if script == "all":
                self.launch_all_components()
                return
            
            if script in self.processes and self.processes[script].poll() is None:
                self.log_message(f"{script} is already running")
                return
            
            # Launch the component
            if script == "aalex.py":
                process = subprocess.Popen([sys.executable, script], 
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                process = subprocess.Popen([sys.executable, script])
            
            self.processes[script] = process
            self.log_message(f"Launched {script} (PID: {process.pid})")
            self.status_label.config(text=f"Running: {script}")
            
        except Exception as e:
            self.log_message(f"Error launching {script}: {str(e)}")
            messagebox.showerror("Launch Error", f"Failed to launch {script}:\n{str(e)}")
    
    def launch_all_components(self):
        """Launch all components"""
        components = ["aalex.py", "aalex_gui.py", "aalex_browser.py"]
        
        for component in components:
            if component not in self.processes or self.processes[component].poll() is not None:
                self.launch_component(component)
                # Small delay between launches
                self.root.after(1000)
        
        self.log_message("All components launched")
        self.status_label.config(text="All components running")
    
    def stop_all_components(self):
        """Stop all running components"""
        stopped_count = 0
        
        for script, process in self.processes.items():
            try:
                if process.poll() is None:  # Process is still running
                    process.terminate()
                    stopped_count += 1
                    self.log_message(f"Stopped {script}")
            except Exception as e:
                self.log_message(f"Error stopping {script}: {str(e)}")
        
        if stopped_count > 0:
            self.log_message(f"Stopped {stopped_count} components")
            self.status_label.config(text="Components stopped")
        else:
            self.log_message("No components were running")
    
    def check_status(self):
        """Check status of all components"""
        running_components = []
        
        for script, process in self.processes.items():
            if process.poll() is None:
                running_components.append(script)
            else:
                # Process has ended, remove from tracking
                del self.processes[script]
        
        if running_components:
            status_text = f"Running: {', '.join(running_components)}"
            self.status_label.config(text=status_text)
            self.log_message(f"Status check: {len(running_components)} components running")
        else:
            self.status_label.config(text="No components running")
            self.log_message("Status check: No components running")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = self.log_text.get("1.0", tk.END).split('\n')
        if len(lines) > 50:
            self.log_text.delete("1.0", f"{len(lines)-50}.0")
    
    def exit_launcher(self):
        """Exit the launcher"""
        if messagebox.askyesno("Exit", "Stop all components and exit?"):
            self.stop_all_components()
            self.root.quit()
    
    def run(self):
        """Run the launcher"""
        # Check for required files
        required_files = ["aalex.py", "aalex_gui.py", "aalex_browser.py"]
        missing_files = [f for f in required_files if not os.path.exists(f)]
        
        if missing_files:
            messagebox.showerror("Missing Files", 
                               f"Required files not found:\n{', '.join(missing_files)}")
            return
        
        self.log_message("AALEX Launcher ready")
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting AALEX Launcher...")
    launcher = AALEXLauncher()
    launcher.run()

if __name__ == "__main__":
    main()
