# AALEX
A comprehensive AI assistant with voice recognition, text-to-speech, system control, and Iron Man-like interface capabilities

## 🚀 Complete System Features

### 🎤 Voice Assistant (aalex.py)
- Wake word detection ("AALEX", "Alex", "Hey AALEX", "Sir")
- Google Speech Recognition for accurate voice commands
- Continuous listening mode
- Natural voice synthesis with male voice preference
- System control (volume, brightness, screenshots, system info)
- Application launcher and web search integration

### 🖥️ GUI Interface (aalex_gui.py) - Ironman style
- **Always-on-top overlay** in top-left corner
- **Notes system** for quick note-taking
- **Code snippets** storage and management
- **Screen analysis** and monitoring

- **ChatGPT integration** for AI responses
- **Social media management** with quick access
- **Transparency controls** and customization
- **Auto-save** functionality

### 🌐 AALEX Browser (aalex_browser.py)
- **Integrated browser** for social media management
- **AI tools** quick access (ChatGPT, Claude, Perplexity, etc.)
- **Social media** management (Twitter, LinkedIn, Facebook, etc.)
- **News feed** integration
- **Developer tools** access
- **Web content** management

### 🚀 Launcher System (aalex_launcher.py)
- **One-click launch** of all components
- **Process management** and monitoring
- **Status tracking** of running components
- **Launch log** for debugging
- **Stop all** functionality

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows 10/11
- Microphone and speakers

### Setup

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd aalex
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install PyAudio (if installation fails)**
   ```bash
   # For Windows, you might need to install from a wheel
   pip install pipwin
   pipwin install pyaudio
   ```

4. **Run AALEX**
   ```bash
   python aalex.py
   ```

## Usage

### Quick Start
1. **Launch everything**: `python aalex_launcher.py`
2. Click "Launch All" to start all components
3. The GUI overlay will appear in the top-left corner
4. Say "AALEX" to activate voice commands

### Individual Components
- **Voice Assistant**: `python aalex.py`
- **GUI Interface**: `python aalex_gui.py`
- **Browser**: `python aalex_browser.py`
- **Launcher**: `python aalex_launcher.py`

### Voice Commands
Say one of the wake words to activate:
- "AALEX"
- "Alex" 
- "Hey AALEX"
- "Jarvis"

### Voice Commands

#### Time & Date
- "AALEX, what time is it?"
- "AALEX, what's the date?"

#### System Control
- "AALEX, volume up/down/mute"
- "AALEX, take a screenshot"
- "AALEX, system information"
- "AALEX, battery status"
- "AALEX, shutdown/restart/sleep computer"

#### Applications
- "AALEX, open notepad/calculator/chrome"
- "AALEX, close [application]"

#### Web & Search
- "AALEX, search for [query]"
- "AALEX, weather information"

#### Entertainment
- "AALEX, tell me a joke"
- "AALEX, tell me a quote"

#### Help
- "AALEX, help" - Shows all available commands

### GUI Interface Features

#### Notes System
- Quick note-taking with timestamps
- Add, delete, and clear notes
- Auto-save functionality

#### Code Snippets
- Store and manage code snippets
- Copy to clipboard functionality
- Syntax highlighting support

#### Screen Analysis
- Real-time screen monitoring
- Application usage tracking
- System performance monitoring
- Screenshot capture

#### ChatGPT Integration
- Direct API integration
- Chat interface
- API key management

#### Social Media Management
- Quick access to all platforms
- Integrated feed management
- One-click platform access

## Configuration

### Voice Settings
You can modify voice settings in the `setup_tts()` method:
- Speech rate (default: 180)
- Volume level (default: 0.9)
- Voice selection (prefers male voices)

### Wake Words
Add or modify wake words in the `wake_words` list:
```python
self.wake_words = ["aalex", "alex", "hey aalex", "jarvis", "your_custom_word"]
```

### Commands
Add new commands by:
1. Adding a method to the `AALEX` class
2. Adding the command to the `commands` dictionary

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   - Install PyAudio: `pip install pyaudio`
   - If that fails, try: `pip install pipwin && pipwin install pyaudio`

2. **Microphone not working**
   - Check microphone permissions in Windows settings
   - Ensure microphone is set as default recording device

3. **Voice recognition not accurate**
   - Speak clearly and at normal volume
   - Reduce background noise
   - Adjust microphone sensitivity in Windows

4. **TTS not working**
   - Check if speakers are working
   - Verify Windows TTS is enabled
   - Try different voice options in the code

### Performance Tips
- Close unnecessary applications for better performance
- Use a good quality microphone for better recognition
- Speak clearly and wait for the beep before giving commands

## Security Notes

- AALEX runs locally on your computer
- Voice data is processed by Google Speech Recognition (sent over internet)
- No personal data is stored or transmitted
- System commands require user confirmation for safety

## Contributing

Feel free to contribute by:
- Adding new voice commands
- Improving voice recognition accuracy
- Adding new system control features
- Enhancing the user interface
- Reporting bugs and issues

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] GUI interface
- [ ] Custom wake word training
- [ ] Integration with smart home devices
- [ ] Calendar and reminder system
- [ ] Email and messaging integration
- [ ] Advanced system monitoring
- [ ] Plugin system for custom commands

