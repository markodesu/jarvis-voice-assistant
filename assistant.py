import speech_recognition as sr
import pyttsx3
import webbrowser
import re
import os
import sys
import platform
import subprocess
import signal
import psutil
import datetime
import random

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for idx, voice in enumerate(voices):
        lang = voice.languages[0].decode('utf-8') if isinstance(voice.languages[0], bytes) else voice.languages[0]
        print(f"{idx}: ID={voice.id}, Name={voice.name}, Lang={lang}, Gender={getattr(voice, 'gender', 'unknown')}")
    engine.stop()

def get_voice_by_preference(engine, preferred_name=None, preferred_id=None):
    voices = engine.getProperty('voices')
    if preferred_id:
        for voice in voices:
            if voice.id == preferred_id:
                return voice.id
    if preferred_name:
        for voice in voices:
            if preferred_name.lower() in voice.name.lower():
                return voice.id
    # fallback: first English male, then first English
    for voice in voices:
        lang = voice.languages[0].decode('utf-8') if isinstance(voice.languages[0], bytes) else voice.languages[0]
        if ('en' in lang) and 'male' in voice.name.lower():
            return voice.id
    for voice in voices:
        lang = voice.languages[0].decode('utf-8') if isinstance(voice.languages[0], bytes) else voice.languages[0]
        if 'en' in lang or 'english' in voice.name.lower():
            return voice.id
    return voices[0].id if voices else None

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.voice.compact.en-GB.Daniel')
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    notes_file = "notes.txt"
    reminders = []
    jokes = [
        "Why did the computer show up at work late? It had a hard drive!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the developer go broke? Because he used up all his cache!",
        "Why was the cell phone wearing glasses? Because it lost its contacts!"
    ]
    while True:
        with mic as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            if "open youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")
            elif "close youtube" in command:
                speak("Closing YouTube")
                if platform.system() == "Darwin":
                    script = '''osascript -e 'tell application "Google Chrome" to close (every tab of every window whose URL contains "youtube.com")' '''
                    os.system(script)
                    script2 = '''osascript -e 'tell application "Safari" to close (every tab of every window whose URL contains "youtube.com")' '''
                    os.system(script2)
            elif "open cursor" in command or "open cursorai" in command:
                speak("Opening Cursor AI")
                webbrowser.open("https://www.cursor.so")
            elif re.search(r"what is|calculate|plus|minus|times|divided by|multiplied by|add|subtract|divide|multiply", command):
                try:
                    expr = command.replace('what is', '').replace('calculate', '')
                    expr = expr.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('multiplied by', '*').replace('divided by', '/').replace('divide', '/').replace('add', '+').replace('subtract', '-').replace('multiply', '*')
                    expr = re.sub(r'[^0-9\+\-\*/\.\(\) ]', '', expr)
                    result = eval(expr)
                    speak(f"The answer is {result}")
                    print(f"Calculation: {expr} = {result}")
                except Exception as e:
                    speak("Sorry, I could not calculate that.")
                    print(f"Calculation error: {e}")
            elif "open video" in command:
                speak("Opening a video on YouTube")
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            elif "settings" in command:
                speak("Settings command recognized. No action implemented.")
            elif "exit" in command or "quit" in command:
                speak("Exiting assistant.")
                break
            elif "time" in command:
                now = datetime.datetime.now().strftime("%H:%M")
                speak(f"The current time is {now}")
            elif "date" in command:
                today = datetime.datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today is {today}")
            elif "joke" in command:
                joke = random.choice(jokes)
                speak(joke)
            elif "search google for" in command:
                query = command.split("search google for")[-1].strip()
                if query:
                    speak(f"Searching Google for {query}")
                    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            elif "take a note" in command or "write a note" in command:
                speak("What should I note?")
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source)
                    note_audio = recognizer.listen(source)
                try:
                    note = recognizer.recognize_google(note_audio)
                    with open(notes_file, "a") as f:
                        f.write(note + "\n")
                    speak("Note saved.")
                except:
                    speak("Sorry, I could not understand the note.")
            elif "read note" in command or "latest note" in command:
                try:
                    with open(notes_file, "r") as f:
                        lines = f.readlines()
                        if lines:
                            speak(f"Your latest note is: {lines[-1].strip()}")
                        else:
                            speak("You have no notes.")
                except:
                    speak("You have no notes.")
            elif "system status" in command or "status" in command:
                cpu = psutil.cpu_percent()
                mem = psutil.virtual_memory().percent
                speak(f"CPU usage is {cpu} percent. Memory usage is {mem} percent.")
            elif "battery" in command:
                if hasattr(psutil, "sensors_battery"):
                    battery = psutil.sensors_battery()
                    if battery:
                        speak(f"Battery is at {battery.percent} percent.")
                    else:
                        speak("Battery information not available.")
                else:
                    speak("Battery information not available.")
            elif "weather" in command:
                speak("Opening weather for your location.")
                webbrowser.open("https://www.google.com/search?q=weather+near+me")
            elif "hello" in command or "hi jarvis" in command or "hey jarvis" in command:
                speak("Hello! How can I help you today?")
            elif "remind me to" in command:
                task = command.split("remind me to")[-1].strip()
                if task:
                    reminders.append(task)
                    speak(f"Reminder set for: {task}")
            elif "what are my reminders" in command or "reminders" in command:
                if reminders:
                    speak("Your reminders are: " + ", ".join(reminders))
                else:
                    speak("You have no reminders.")
            elif "play music" in command:
                speak("Opening YouTube Music.")
                webbrowser.open("https://music.youtube.com/")
            else:
                speak("Command not recognized.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

def main():
    # list_voices()  # No need to print voices every time now
    listen_for_commands()
    print("Assistant stopped.")

if __name__ == "__main__":
    main() 