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
import pyautogui
import subprocess
import cursor
from pipes import quote
from engine.command import all_commands
from engine.helper import extract_yt_term, markdown_to_text, remove_words
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

def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        
        # Use the correct path to jarvis.db in the engine folder
        import os
        db_path = os.path.join('engine', 'jarvis.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Search for contact by name (case-insensitive)
        cursor.execute("SELECT name, mobile_no FROM contacts WHERE LOWER(name) = LOWER(?) OR LOWER(name) LIKE ?", 
                      (query, '%' + query + '%'))
        results = cursor.fetchall()
        
        print(f"Search results for '{query}': {results}")
        
        if not results:
            speak(f"{query} not exist in contacts")
            conn.close()
            return 0, 0
            
        # Get the first matching contact
        contact_name = results[0][0]
        mobile_number = results[0][1]
        
        if not mobile_number:
            speak(f"{contact_name} does not have a phone number in contacts")
            conn.close()
            return 0, 0
            
        # Clean the mobile number and ensure it has country code
        # Remove any spaces, dashes, parentheses
        import re
        mobile_number_str = re.sub(r'[\s\-\(\)]', '', str(mobile_number))
        
        # IMPORTANT: Add +86 if it's a Chinese number (starts with 1 and is 11 digits)
        # but doesn't have the + prefix
        if mobile_number_str and not mobile_number_str.startswith('+'):
            # If it's a valid Chinese number (11 digits starting with 1)
            if re.match(r'^1\d{10}$', mobile_number_str):
                mobile_number_str = f'+86{mobile_number_str}'
            # If it already has 86 at start but no +, add the +
            elif mobile_number_str.startswith('86') and len(mobile_number_str) == 13:
                mobile_number_str = f'+{mobile_number_str}'
        
        print(f"Found contact: {contact_name}, Formatted Number: {mobile_number_str}")
        conn.close()
        return mobile_number_str, contact_name
        
    except Exception as e:
        print(f"Error in findContact: {e}")
        import traceback
        traceback.print_exc()
        speak('Error finding contact')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    from pipes import quote
    encoded_message = quote(message)
    print(encoded_message)
    
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    import subprocess
    import time
    import pyautogui
    
    # Remove the duplicate call - only open once
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    
    # Wait for the message to be typed
    time.sleep(3)
    
    # Press Enter only once to send
    pyautogui.press('enter')
    
    speak(jarvis_message)

def makeCall(name, mobileNo):
    import subprocess
    import time
    import re
    
    # Clean the number - remove any non-digit except '+'
    mobileNo = re.sub(r'[^\d+]', '', str(mobileNo))
    
    # Ensure the number has the country code
    if mobileNo and not mobileNo.startswith('+'):
        # If it's a Chinese number (starts with 1 and is 11 digits)
        if re.match(r'^1\d{10}$', mobileNo):
            mobileNo = f'+86{mobileNo}'
        # If it has 86 but no +, add +
        elif mobileNo.startswith('86') and len(mobileNo) == 12:
            mobileNo = f'+{mobileNo}'
    
    speak(f"Calling {name}")
    print(f"Calling {name} at {mobileNo}")
    
    # Open dialer with the number (use tel: prefix with the full number)
    subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.CALL', '-d', f'tel:{mobileNo}'], capture_output=True)
    time.sleep(2)
    
    # Some phones need the call button to be pressed
    # Try tapping the call button if the dialer doesn't auto-dial
    # subprocess.run(['adb', 'shell', 'input', 'tap', '540', '1800'], capture_output=True)

def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent
    import subprocess
    import time
    
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    
    print(f"DEBUG - Full message to send: '{message}'")
    
    print("Step 1: Going back to home")
    goback(4)
    time.sleep(1)
    
    print("Step 2: Pressing home button")
    keyEvent(3)
    time.sleep(1)
    
    print("Step 3: Opening messaging app with contact")
    subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', f'sms:{mobileNo}'], capture_output=True)
    time.sleep(3)
    
    print("Step 4: Waiting for conversation to open")
    time.sleep(2)
    
    print(f"Step 5: Typing message: {message}")
    # Type the message word by word to handle spaces properly
    words = message.split()
    for i, word in enumerate(words):
        subprocess.run(['adb', 'shell', 'input', 'text', word], capture_output=True)
        if i < len(words) - 1:
            subprocess.run(['adb', 'shell', 'input', 'keyevent', '62'], capture_output=True)  # Space key
            time.sleep(0.1)
    
    time.sleep(1)
    
    print("Step 6: Sending message")
    # Tap the send button at the correct coordinates
    subprocess.run(['adb', 'shell', 'input', 'tap', '988', '1451'], capture_output=True)
    time.sleep(2)
    
    speak("message send successfully to " + name)

from google import genai

def geminai(query):
    try:
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")
        
        # Use your working API key
        client = genai.Client(api_key="AIzaSyC2IizbfZ3_q2E-CDnxc5QHufJChEIW-DY")  # Your working key
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # This model works!
            contents=query
        )
        
        clean_text = markdown_to_text(response.text)
        speak(clean_text)
        return clean_text
        
    except Exception as e:
        print(f"Error in geminai: {e}")
        error_msg = "Sorry, I encountered an error while processing your request."
        speak(error_msg)
        return error_msg
# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name