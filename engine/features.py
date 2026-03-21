from playsound import playsound
import eel
from engine.configuration import ASSISTANT_NAME
from engine.command import speak
import os
import pywhatkit as kit
import webbrowser
import sqlite3
import re
from engine.helper import extract_yt_term
import pvporcupine
import pyaudio
import struct
import time
from engine.command import all_commands
# Initialize database connection (you might already have this elsewhere)
DB_PATH = "engine/jarvis.db"  # Adjust path as needed

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

#play sound 
@eel.expose
def play_sound():
    music_dir = "website/assets/texllate/audio/start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    """Open applications or websites based on voice command"""
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()
    
    # Check if it's a YouTube command first
    if "youtube" in query:
        handle_youtube_command(query)
        return
    
    if query != "":
        app_name = query
        
        try:
            # Try to connect to database
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # First, check in sys_command for local applications
                cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = LOWER(?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening " + app_name)
                    os.startfile(results[0][0])
                else:
                    # If not found in sys_command, check in web_command for websites
                    cursor.execute('SELECT url FROM web_command WHERE LOWER(name) = LOWER(?)', (app_name,))
                    results = cursor.fetchall()
                    
                    if len(results) != 0:
                        speak("Opening " + app_name)
                        webbrowser.open(results[0][0])
                    else:
                        # If not in database, try to open as a Windows app
                        speak("Opening " + app_name)
                        try:
                            os.system('start ' + app_name)
                        except Exception as e:
                            speak("Application not found")
                            print(f"Error opening {app_name}: {e}")
                
                conn.close()
            else:
                # Fallback if database connection fails
                speak("Opening " + query)
                os.system("start " + query)
                
        except sqlite3.Error as e:
            speak("Something went wrong with the database")
            print(f"Database error: {e}")
            # Fallback method
            try:
                os.system('start ' + query)
            except:
                speak("Not found")
    else:
        speak("What would you like to open?")

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

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","computer"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()