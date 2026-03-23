from email.mime import audio

import pyttsx3
import speech_recognition as sr
import eel
import time

def speak(text):
    text = str(text).lower()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.show_message(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.show_message("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 60)

    try:
        print("Recognizing...")
        eel.show_message("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.show_message(query)
        time.sleep(2)
        
    except Exception as e:
        
        return ""
    return query.lower()

@eel.expose
def all_commands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        
        # Check for YouTube-related commands FIRST
        if "youtube" in query:
            from engine.features import handle_youtube_command
            handle_youtube_command(query)
        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
        else:
            from engine.features import chatBot
            chatBot(query)
            
    except Exception as e:
       print("Actual error:", e)
       eel.show_hood()