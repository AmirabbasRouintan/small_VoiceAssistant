import speech_recognition as sr
import os
import cowsay
from datetime import datetime
from gtts import gTTS
import playsound
import subprocess

PURPLE = "\033[38;2;189;147;249m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

def speak(text):
    """Speaks the given text using Google Text-to-Speech."""
    tts = gTTS(text=text, lang='en')
    filename = "output.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def speak_time():
    current_time = datetime.now()
    print("Current Time:", current_time.strftime("%H:%M:%S"))
    current_time = datetime.now().strftime('%H:%M:%S')
    message = f"The current time is {current_time}"
    tts = gTTS(text=message, lang='en')
    filename = "time.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def run_command(command):
    """Run a shell command and print the output."""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error executing command: {e}{RESET}")

def open_application(app_name):
    """Open a specified application."""
    app_commands = {
        "brave": "brave",
        "music": "audacious",
        "file manager" : "thunar"
    }
    command = app_commands.get(app_name.lower())
    if command:
        print(f"{YELLOW}Opening {app_name}...{RESET}")
        run_command(command)
    else:
        print(f"{RED}Bot: I can't open {app_name}.{RESET}")

def close_application(app_name):
    """Close a specified application."""
    app_commands = {
        "brave": "brave",
        "music": "audacious",
        "file manager" : "thunar"
    }
    command = app_commands.get(app_name.lower())
    if command:
        print(f"{YELLOW}Closing {app_name}...{RESET}")
        run_command(f"pkill {command.split()[0]}")  
        print(f"{RED}Bot: I can't close {app_name}.{RESET}")


def real_time_transcription():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        os.system("clear")
        cowsay.milk("Listening... (Press Ctrl+C to stop)")
        r.adjust_for_ambient_noise(source)
        
        sleeping = False
        
        try:
            while True:
                if not sleeping:
                    audio = r.listen(source)
                    try:
                        text = r.recognize_google(audio)
                        print(f"{YELLOW}YOU: {text}{RESET}")

                        if text == "show me the calendar" or text == "show me calendar" or "calendar" in text: 
                            os.system("clear && cal && echo '------------------------' && jcal")
                        if text == "my ai" or text == "my AI" or text == "open my AI": 
                            os.system("bash ~/.config/rofi/web_things/ai.sh")
                        if text == "what is your name" or text == "what's your name" : 
                            cowsay.fox(f"{RED}My name is {PURPLE}flower{RED} bot{RESET}")
                            message = f"My name is flower bot" 
                            tts = gTTS(text=message, lang='en')
                            filename = "name.mp3"
                            tts.save(filename)
                            playsound.playsound(filename)
                            os.remove(filename)
                        if any(phrase in text for phrase in ["what you can do", "help commands", "help command", "your option", "what can you do"]):
                            cowsay.fox("clear terminal\n write the commands")
                        if any(phrase in text for phrase in ["what time is it", "time"]):          
                            speak_time()
                        if "run this command" in text.lower():
                            cowsay.fox(f"{YELLOW}Listening for command to run...{RESET}")
                            audio = r.listen(source)
                            command_text = r.recognize_google(audio).lower()
                            print(f"{YELLOW}Command: {command_text}{RESET}")
                            
                            if "n e o fetch" in command_text or "neofetch" in command_text or "neo fetch":
                                run_command("neofetch")
                            else:
                                print(f"{RED}Bot: I can't run that command.{RESET}")
                        if "how are you" in text.lower(): 
                            cowsay.fox(f"{RED}Bot: I'm good, thank you!{RESET}")
                        elif "hello" in text.lower() or "hi" in text.lower():
                            cowsay.fox(f"{RED}Bot: Hello! How can I assist you today?{RESET}")
                        elif "clear terminal" in text.lower() or "clear" in text:
                            clear_terminal()
                        elif any(phrase in text.lower() for phrase in ["go sleep", "go to sleep", "sleep"]):
                            print(f"{PURPLE}Bot: Going to sleep...{RESET}")
                            sleeping = True
                        elif "open" in text.lower():
                            app_name = text.lower().replace("open ", "")
                            open_application(app_name)
                        elif "kill" in text.lower() or "close" in text.lower():
                            app_name = text.lower().replace("kill ", "").replace("close ", "")
                            close_application(app_name)
                        
                    except sr.UnknownValueError:
                        print("Sorry, I could not understand the audio.")
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
                
                else:
                    cowsay.milk(f"{PURPLE}Bot is sleeping... Say 'hey wake up' to wake up.{RESET}")
                    audio = r.listen(source)
                    try:
                        text = r.recognize_google(audio)
                        print(f"{YELLOW}YOU: {text}{RESET}")
                        
                        if "hey wake up" in text.lower():
                            print(f"{RED}Bot: Waking up!{RESET}")
                            sleeping = False
                        
                    except sr.UnknownValueError:
                        continue
                    except sr.RequestError as e:
                        print(f"Could not request results from Google Speech Recognition service; {e}")
        
        except KeyboardInterrupt:
            cowsay.cow("\nStopped listening.")

if __name__ == "__main__":
    real_time_transcription()
