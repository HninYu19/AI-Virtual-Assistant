import pyttsx3
import speech_recognition as sr
import eel
import time

@eel.expose
def show_message(message):
    """Show status message in the UI"""
    print(f"Status message: {message}")
    try:
        eel.show_message(message)
        eel.show_status_message(message)
        print(f"Sent to JS: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

def speak(text):
    text = str(text).lower()
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    
    # Show the message being spoken
    print(f"Speaking: {text}")
    eel.show_message(text)
    eel.receiverText(text)  # This sends to chat
    eel.senderText(f"Jarvis: {text}")  # Alternative display
    
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        show_message("🎤 Listening...")
        
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Audio captured successfully")
            show_message("✅ Audio captured")
        except sr.WaitTimeoutError:
            print("Listening timed out")
            show_message("⏱️ No input detected")
            eel.receiverText("I didn't hear anything. Please try again.")
            return ""

    try:
        print("Recognizing...")
        show_message("🔄 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        show_message(f"✅ Recognized: {query[:50]}...")
        
        # Send user command to chat
        eel.senderText(query)
        time.sleep(1)
        return query.lower()
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        show_message("❌ Could not understand")
        eel.receiverText("I couldn't understand that. Please try again.")
        return ""
    
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        show_message("❌ Speech service error")
        eel.receiverText("There was a problem with the speech recognition service.")
        return ""

@eel.expose
def all_commands(message=None):
    print(f"all_commands called with message: {message}")
    eel.ShowSiriWave()
    
    # If no message provided, listen for voice command
    if message is None or message == 1 or message == "":
        print("Listening for voice command...")
        show_message("🎤 Listening for command...")
        query = takecommand()
        print(f"Voice command result: '{query}'")
        
        if query and query.strip():
            show_message(f"📝 Command: {query}")
            # User command already sent in takecommand, but ensure it's there
        else:
            print("No voice command detected")
            show_message("❌ No command detected")
            eel.receiverText("I didn't hear anything. Please try again.")
            return "No command detected"
    else:
        # Text command from chat
        print(f"Processing text command: {message}")
        query = message
        show_message(f"📝 Processing: {query}")
        eel.senderText(query)

    # Check for exit/back to main screen commands FIRST
    if any(phrase in query for phrase in ["go back to main screen", "exit", "home", "main screen", "go to home", "back to home", "close"]):
        print("Going back to main screen")
        speak("Returning to main screen")
        eel.goToMainScreen()
        return "Returning to main screen"
    
    try:
        show_message("⚙️ Processing command...")
        # Check for YouTube-related commands FIRST
        if "youtube" in query:
            from engine.features import handle_youtube_command
            handle_youtube_command(query)
        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
        # Check for CALL commands
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
            from engine.features import geminai
            geminai(query)
        
        show_message("✅ Command completed")
            
    except Exception as e:
        print(f"Error processing command: {e}")
        import traceback
        traceback.print_exc()
        show_message(f"❌ Error: {str(e)[:50]}")
        eel.receiverText(f"Sorry, an error occurred: {str(e)}")
    
    return "Command processed"