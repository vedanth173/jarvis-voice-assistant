import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
    text = str(text)
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices') 
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 174)
        try:
            eel.DisplayMessage(text)
        except Exception:
            pass
        engine.say(text)
        try:
            eel.receiverText(text)
        except Exception:
            pass
        engine.runAndWait()
    except Exception as e:
        print(f"speak error: {e}")


def takecommand():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print('listening....')
            try:
                eel.DisplayMessage('listening....')
            except Exception:
                pass
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio = r.listen(source, 10, 6)
    except Exception as e:
        print(f"Microphone error: {e}")
        try:
            eel.DisplayMessage('Microphone unavailable')
        except Exception:
            pass
        return ""

    try:
        print('recognizing....')
        try:
            eel.DisplayMessage('recognizing....')
        except Exception:
            pass
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        try:
            eel.DisplayMessage(query)
        except Exception:
            pass
        time.sleep(1)
        return query.lower()
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return ""


def sendMessage(message, contact_no, name):
    speak(f"Mobile SMS is not currently supported. Please use WhatsApp to message {name}.")


def makeCall(name, contact_no):
    speak(f"Direct phone calls are not currently supported. Please use WhatsApp to call {name}.")


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        if not query or query.strip() == "":
            try:
                eel.ShowHood()
            except Exception:
                pass
            return
        print(f"Voice query: {query}")
        try:
            eel.senderText(query)
        except Exception:
            pass
    else:
        query = str(message).lower().strip()
        if not query:
            try:
                eel.ShowHood()
            except Exception:
                pass
            return
        print(f"Text query: {query}")
        try:
            eel.senderText(query)
        except Exception:
            pass

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsapp
            contact_no, name = findContact(query)
            if contact_no != 0:
                speak("Which mode would you like to use: WhatsApp or mobile?")
                preference = takecommand()
                print(f"Preference: {preference}")

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query: 
                        speak("What message would you like to send?")
                        msg_text = takecommand()
                        sendMessage(msg_text, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again.")
                elif "whatsapp" in preference or "what's app" in preference:
                    flag = "message"
                    if "phone call" in query:
                        flag = 'call'
                    elif "video call" in query:
                        flag = 'video call'
                    else:
                        speak("What message would you like to send?")
                        query = takecommand()
                                        
                    whatsapp(contact_no, query, flag, name)
                else:
                    speak("Mode not recognized, canceling action.")
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print("Error executing command:", e)
        try:
            eel.DisplayMessage('Error: ' + str(e))
        except Exception:
            pass
    
    try:
        eel.ShowHood()
    except Exception:
        pass