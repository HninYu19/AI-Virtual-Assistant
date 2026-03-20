from playsound import playsound
import eel

#play sound 
@eel.expose
def play_sound():
    music_dir = "website/assets/texllate/audio/start_sound.mp3"
    playsound(music_dir)