from playsound import playsound
import eel
from engine.configuration import ASSISTANT_NAME
from engine.command import speak
import os
import pywhatkit as kit
import webbrowser
import re

#play sound 
@eel.expose
def play_sound():
    music_dir = "website/assets/texllate/audio/start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace("ASSISTANT_NAME", "")
    query = query.replace("open", "")
    query.lower()

    if query != "":
        speak("Opening "+query)
        os.system("start "+query)
    else:
        speak("Not Found")

def PlayYoutube(query):
   search_term = extract_yt_search_term(query)
   speak("Playing "+search_term+" on YouTube")
   kit.playonyt(search_term)

def extract_yt_search_term(command):
    pattern = r"play\s+(.*?)\s+on\s+youtube"
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None