import multiprocessing
import subprocess
import sys
import os
import time

# Import face recognition
from engine.auth import recoganize

def close_camera_app():
    """Force close the Windows Camera app"""
    try:
        subprocess.run(['taskkill', '/f', '/im', 'WindowsCamera.exe'], capture_output=True)
        subprocess.run(['taskkill', '/f', '/im', 'Microsoft.WindowsCamera.exe'], capture_output=True)
        print("✅ Camera app closed")
    except:
        pass

# To run Jarvis
def startJarvis():
    # Code for process 1
    print("Process 1 is running.")
    from main import start
    start()

# To run hotword
def listenHotword():
    # Code for process 2
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()

# Start both processes
if __name__ == '__main__':
    print("=" * 60)
    print("🔐 AI Virtual Assistant - Face Recognition Security")
    print("=" * 60)
    
    # STEP 1: Authenticate face FIRST
    print("\n📸 Face authentication required...")
    print("-" * 60)
    
    auth_result = recoganize.AuthenticateFace()
    
    # Close camera app immediately after authentication
    close_camera_app()
    
    # Check if authentication was successful
    if auth_result == 1:
        print("\n" + "=" * 60)
        print("✅ Authentication Successful! Starting Assistant...")
        print("=" * 60)
        
        # STEP 2: Run the batch file to set up the environment
        print("\n🔄 Setting up device environment...")
        subprocess.call([r'device.bat'])
        
        # STEP 3: Start both processes
        print("🔄 Starting Jarvis and Hotword detection...")
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        
        p1.start()
        p2.start()
        p1.join()
        
        if p2.is_alive():
            p2.terminate()
            p2.join()
        
        print("\n" + "=" * 60)
        print("🛑 System is shutting down...")
        print("=" * 60)
        
    else:
        print("\n" + "=" * 60)
        print("❌ Authentication Failed! Access Denied.")
        print("=" * 60)
        print("\nSystem will not start. Please try again.")
        sys.exit(1)