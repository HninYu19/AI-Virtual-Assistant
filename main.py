import os
import eel
import multiprocessing
import subprocess
import sys
import time

from engine.features import *
from engine.command import *
from engine.auth import recoganize

def start():

    eel.init('website')

    play_sound()

    @eel.expose
    def start_authentication():
        """Start face authentication process"""
        print("Starting face authentication from web...")
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticationFace()  # Make sure this function exists
        if flag == 1:
            speak("Face Authentication Successful")
            return {"success": True, "message": "Authentication successful"}
        else:
            speak("Face Authentication Failed")
            return {"success": False, "message": "Authentication failed"}
    
    @eel.expose
    def close_camera():
        """Close camera after authentication"""
        try:
            subprocess.run(['taskkill', '/f', '/im', 'WindowsCamera.exe'], capture_output=True)
            subprocess.run(['taskkill', '/f', '/im', 'Microsoft.WindowsCamera.exe'], capture_output=True)
            print("Camera closed")
            return True
        except Exception as e:
            print(f"Error closing camera: {e}")
            return False
    
    # Don't call authentication here - let HTML handle it
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)

def startJarvis():
    """Start the main Jarvis application"""
    from main import start
    start()

def listenHotword():
    """Start hotword detection"""
    from engine.features import hotword
    hotword()

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 AI Virtual Assistant - Starting Interface...")
    print("=" * 60)
    
    # Start both processes
    print("🔄 Starting Jarvis and Hotword detection...")
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)
    
    p1.start()
    p2.start()
    p1.join()
    
    if p2.is_alive():
        p2.terminate()
        p2.join()