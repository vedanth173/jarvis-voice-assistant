from urllib.parse import quote as url_quote
# Clipboard support: prefer pyperclip if available, otherwise fall back to tkinter
try:
    import pyperclip
    _HAS_PYPERCLIP = True
except Exception:
    _HAS_PYPERCLIP = False
import struct
import subprocess
import sys, os
import time
import pvporcupine
import pyaudio
import pyautogui
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import re
from playsound import playsound
from engine.command import speak  
from engine.config import ASSISTANT_NAME 
import eel
import pywhatkit as kit
import webbrowser
import sqlite3
from engine.helper import extract_yt_term, remove_words


from hugchat import hugchat 

# Initialize database connection
try:
    print("\n=== Initializing Database Connection ===")
    con = sqlite3.connect('jarvis.db')
    cursor = con.cursor()
    
    # Test the connection
    cursor.execute("SELECT COUNT(*) FROM contacts")
    count = cursor.fetchone()[0]
    print(f"Database connected successfully. Found {count} contacts.")
    
except sqlite3.Error as e:
    print(f"Database Error: {str(e)}")
    print("Make sure jarvis.db exists and has the contacts table")


@eel.expose
def playAssistantSound():
   music_dir = "C:\\Users\\sudee\\Downloads\\PPROJECT\\www\\assets\\audio\\start_sound.mp3"
   playsound(music_dir)
   
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()
    
    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                target = results[0][0]
                # If the stored path is a URL, open it in the browser instead of trying to execute it
                try:
                    if isinstance(target, str):
                        if target.lower().endswith('whatsapp.exe'):
                            # Always use startfile for WhatsApp desktop app
                            os.startfile(target)
                        elif (target.startswith('http://') or target.startswith('https://') or target.startswith('whatsapp://') or target.startswith('wa.me')):
                            webbrowser.open(target)
                        else:
                            # Assume it's a local executable path
                            os.startfile(target)
                except Exception as e:
                    print(f"Error opening target: {str(e)}")
                    speak('Could not open the requested application or URL')

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("something went wrong")
@eel.expose
    
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    pattern= r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command,re.IGNORECASE)
    return match.group(1) if match else None






#hotword cde is to be ADDED LATER
def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
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






# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0












#### 9. Create Whatsapp Function in features.py



def whatsapp(mobile_no, message, flag, name):

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
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
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
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
