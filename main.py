import os
import eel

from engine.features import *
from engine.command import *
# Remove: from engine.auth import recoganize

def start():
    eel.init('website')
    play_sound()  # Make sure to call the function with parentheses
    # Remove the authentication call from here
    # flag = recoganize.AuthenticateFace()  # DELETE THIS LINE
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)