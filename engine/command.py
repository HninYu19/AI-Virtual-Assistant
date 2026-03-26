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
        
        audio = r.listen(source, 10, 6)

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
        # Check for CALL commands (add this section)
        elif any(phrase in query for phrase in ["call", "phone call", "video call"]):
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode do you want to use? WhatsApp or mobile?")
                preference = takecommand()
                print(f"User preference: {preference}")

                if "mobile" in preference:
                    speak(f"Calling {name} via mobile")
                    makeCall(name, contact_no)
                elif "whatsapp" in preference:
                    # Check if it's video call or voice call
                    if "video" in query:
                        speak(f"Starting video call with {name} on WhatsApp")
                        whatsApp(contact_no, '', 'video call', name)
                    else:
                        speak(f"Calling {name} on WhatsApp")
                        whatsApp(contact_no, '', 'call', name)
                else:
                    speak("Please specify WhatsApp or mobile")
        # Check for message/send commands
        elif any(phrase in query for phrase in ["send message", "message to", "text to", "send sms", "message"]):
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode do you want to use? WhatsApp or mobile?")
                preference = takecommand()
                print(f"User preference: {preference}")

                if "mobile" in preference:
                    speak("What message would you like to send?")
                    message_text = takecommand()
                    if message_text:
                        sendMessage(message_text, contact_no, name)
                elif "whatsapp" in preference:
                    speak("What message would you like to send?")
                    message_text = takecommand()
                    if message_text:
                        whatsApp(contact_no, message_text, 'message', name)
                else:
                    speak("Please specify WhatsApp or mobile")
        else:
            from engine.features import chatBot
            chatBot(query)
            
    except Exception as e:
       print("Actual error:", e)
       import traceback
       traceback.print_exc()
       eel.show_hood()