# Jarvis-like Voice Assistant for macOS

This project is a simple, extensible voice assistant inspired by Jarvis from Iron Man, designed to run on macOS. It uses your microphone to listen for commands and responds with a natural-sounding English male voice. The assistant can:

## Features
- Open and close YouTube
- Open CursorAI
- Perform simple calculations ("what is 2 plus 2")
- Tell the current time and date
- Tell a joke
- Search Google by voice
- Take and read notes
- Give system status (CPU, memory, battery)
- Check the weather (via web search)
- Greet the user
- Set and read reminders
- Play music (YouTube Music)
- And more!

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/markodesu/jarvis-voice-assistant.git
   cd jarvis-voice-assistant
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the assistant:**
   ```bash
   python assistant.py
   ```

## Usage
- Speak commands like "open YouTube", "what time is it?", "tell me a joke", etc.
- The assistant will respond with voice and perform the requested action.
- To stop the assistant, say "exit" or press Ctrl+C.

## Notes
- This project is for educational and personal use.
- Works best on macOS with a working microphone and speakers.
- The assistant uses the Daniel (en-GB) voice by default for natural English male speech.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License 