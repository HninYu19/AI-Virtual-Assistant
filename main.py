import os
import eel
import sys
import subprocess
import traceback

from engine.features import *
from engine.command import *
from engine.auth import recoganize

def start():
    # Set up Eel with proper error handling
    eel.init("website", allowed_extensions=['.js', '.html', '.css', '.mp3'])
    
    @eel.expose
    def init():
        print("init function called")
        try:
            play_sound()
            subprocess.call([r'device.bat'], shell=True)
            eel.hideLoader()
            speak("Ready for Face Authentication")
            flag = recoganize.AuthenticateFace()
            if flag == 1:
                eel.hideFaceAuth()
                speak("Face Authentication Successful")
                eel.hideFaceAuthSuccess()
                speak("Hello, Welcome Sir, How can i Help You")
                eel.hideStart()
                play_sound()
            else:
                speak("Face Authentication Fail")
                eel.receiverText("Face authentication failed. Please try again.")
        except Exception as e:
            print(f"Error in init: {e}")
            traceback.print_exc()
            speak("An error occurred during initialization")
    
    # Make sure all_commands is exposed from features
    if 'all_commands' in globals():
        print("all_commands function found")
    else:
        print("WARNING: all_commands function not found")
    
    # Open browser
    try:
        os.system('start msedge.exe --app="http://localhost:8000/index.html"')
        print("Browser opened with Edge")
    except:
        try:
            os.system('start chrome.exe --app="http://localhost:8000/index.html"')
            print("Browser opened with Chrome")
        except:
            print("Failed to open browser automatically")
    
    # Start Eel with proper error handling
    try:
        print("Starting Eel on http://localhost:8000")
        eel.start('index.html', 
                  mode=None, 
                  host='localhost', 
                  port=8000,
                  block=True,
                  size=(1200, 800))
    except Exception as e:
        print(f"Error starting Eel: {e}")
        traceback.print_exc()
        sys.exit(1)