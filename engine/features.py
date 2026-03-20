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
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()

    if "youtube" in query:
        # This will be handled by handle_youtube_command now
        pass
    elif query != "":
        speak("Opening "+query)
        os.system("start "+query)
    else:
        speak("Not Found")

def handle_youtube_command(query):
    """Handle all YouTube-related commands"""
    # Extract search term from various patterns
    search_term = extract_search_term(query)
    
    if search_term:
        # If there's something to search, play it
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    else:
        # If just "open youtube" or "youtube", open homepage
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

def extract_search_term(command):
    """Extract what to search on YouTube from the command"""
    command = command.lower()
    
    # Remove common phrases
    phrases_to_remove = [
        "open", "play", "from youtube", "on youtube", 
        "youtube", "please", "can you", "could you"
    ]
    
    search_term = command
    
    # Remove each phrase
    for phrase in phrases_to_remove:
        search_term = search_term.replace(phrase, "")
    
    # Clean up extra spaces
    search_term = search_term.strip()
    
    # If nothing is left, return None (just open YouTube)
    if not search_term or search_term == "":
        return None
    
    # Handle specific patterns
    # Pattern: "taylor swift from youtube" -> "taylor swift"
    if " from " in command:
        parts = command.split(" from ")
        if parts:
            search_term = parts[0].replace("open", "").replace("play", "").strip()
    
    # Pattern: "open taylor swift on youtube" -> "taylor swift"
    if " on " in command and "youtube" in command:
        parts = command.split(" on ")
        if parts:
            search_term = parts[0].replace("open", "").replace("play", "").strip()
    
    # If search term is still empty or just "youtube", return None
    if search_term in ["", "youtube"]:
        return None
    
    return search_term

def PlayYoutube(query):
    handle_youtube_command(query)