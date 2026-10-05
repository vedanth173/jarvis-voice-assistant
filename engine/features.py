import os
import sys
import time
import re
import struct
import subprocess
import sqlite3
import webbrowser
from urllib.parse import quote

# Ensure parent directory is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Clipboard support: prefer pyperclip if available, otherwise fall back to tkinter
try:
    import pyperclip
    _HAS_PYPERCLIP = True
except Exception:
    _HAS_PYPERCLIP = False

import pvporcupine
import pyaudio
import pyautogui
from playsound import playsound
import eel
import pywhatkit as kit

from engine.command import speak  
from engine.config import ASSISTANT_NAME, PORCUPINE_ACCESS_KEY
from engine.helper import extract_yt_term, remove_words

try:
    from hugchat import hugchat
    _HAS_HUGCHAT = True
except Exception:
    _HAS_HUGCHAT = False

# Initialize database connection
DB_PATH = os.path.join(BASE_DIR, "jarvis.db")
try:
    print("\n=== Initializing Database Connection ===")
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    
    # Test the connection
    cursor.execute("SELECT COUNT(*) FROM contacts")
    count = cursor.fetchone()[0]
    print(f"Database connected successfully. Found {count} contacts.")
    
except sqlite3.Error as e:
    print(f"Database Error: {str(e)}")
    print(f"Make sure jarvis.db exists at {DB_PATH} and has the contacts table")


@eel.expose
def playAssistantSound():
    music_dir = os.path.join(BASE_DIR, "www", "assets", "audio", "start_sound.mp3")
    if os.path.exists(music_dir):
        try:
            playsound(music_dir)
        except Exception as e:
            print(f"Audio playback notice: {e}")
    else:
        print(f"Sound file not found at: {music_dir}")

   
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()
    
    app_name = query

    if app_name != "":
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening " + query)
                target = results[0][0]
                # If the stored path is a URL, open it in the browser instead of trying to execute it
                try:
                    if isinstance(target, str):
                        if target.lower().endswith('whatsapp.exe'):
                            os.startfile(target)
                        elif (target.startswith('http://') or target.startswith('https://') or target.startswith('whatsapp://') or target.startswith('wa.me')):
                            webbrowser.open(target)
                        else:
                            os.startfile(target)
                except Exception as e:
                    print(f"Error opening target: {str(e)}")
                    speak('Could not open the requested application or URL')

            elif len(results) == 0: 
                cursor.execute(
                    'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except Exception:
                        speak("not found")
        except Exception as e:
            print(f"openCommand error: {e}")
            speak("something went wrong")


@eel.expose
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("What would you like me to play on YouTube?")


def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None


def hotword():
    """Listens for wake words (e.g. 'Jarvis', 'Alexa') using Porcupine."""
    if not PORCUPINE_ACCESS_KEY:
        print("\n[NOTE] Picovoice AccessKey is not set in engine/config.py.")
        print("Hotword detection ('Jarvis', 'Alexa') is disabled.")
        print("You can activate Jarvis using the mic button in the UI or by pressing Win+J.\n")
        return

    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(access_key=PORCUPINE_ACCESS_KEY, keywords=["jarvis", "alexa"]) 
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        print("Hotword listener running. Say 'Jarvis' or 'Alexa' to activate...")
        
        while True:
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Hotword detected!")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
                
    except Exception as e:
        print(f"[Hotword Notice] Hotword listener stopped: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        if results and len(results) > 0:
            print(results[0][0])
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            return mobile_number_str, query
        else:
            speak('Contact not found')
            return 0, 0
    except Exception as e:
        print(f"findContact error: {e}")
        speak('not exist in contacts')
        return 0, 0


def whatsapp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = "message sent successfully to " + name
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling " + name
    else:
        target_tab = 6
        message = ''
        jarvis_message = "starting video call with " + name

    encoded_message = quote(message)
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)


# chat bot 
def chatBot(query):
    user_input = query.lower().strip()
    if not user_input:
        return ""
        
    try:
        cookie_path = os.path.join(BASE_DIR, "engine", "cookies.json")
        if not os.path.exists(cookie_path) or not _HAS_HUGCHAT:
            raise RuntimeError("HuggingChat or cookies.json not configured")

        chatbot = hugchat.ChatBot(cookie_path=cookie_path)
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response
    except Exception as e:
        print(f"ChatBot notice: {e}")
        msg = f"I heard you say: {query}. However, my AI chatbot service is currently offline. Please configure your HugChat cookies or try another voice command."
        speak(msg)
        return msg
