import os
import re
import random
import datetime
import wikipedia
import pyautogui

try:
    from google import genai
    _HAS_GENAI = True
except Exception:
    _HAS_GENAI = False

from engine.config import ASSISTANT_NAME, GEMINI_API_KEY

# Set custom user agent for Wikipedia queries
wikipedia.set_user_agent("JarvisAssistant/1.0 (contact: support@jarvis.local)")

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache!",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "Why do Java developers wear glasses? Because they don't C sharp!",
    "A SQL query walks into a bar, walks up to two tables, and asks: Can I join you?",
    "Why was the computer cold? It left its Windows open!",
    "Real programmers count from 0, not 1."
]

GREETING_RESPONSES = [
    "Hello sir! How can I assist you today?",
    "Greetings! All systems are online and ready for your command.",
    "Hi there! What can I do for you today, sir?",
    "Hello! Ready when you are."
]

STATUS_RESPONSES = [
    "I am functioning at full capacity and ready to assist you, sir!",
    "All diagnostics are green. Ready for your command!",
    "I am doing great! How can I help you today?"
]

IDENTITY_RESPONSES = [
    f"I am {ASSISTANT_NAME.upper()}, your personal desktop voice assistant.",
    f"My name is {ASSISTANT_NAME.upper()}. I am designed to help automate your daily tasks, launch apps, play music, and answer questions."
]


def ask_gemini(prompt: str) -> str:
    """Queries Google Gemini AI if GEMINI_API_KEY is configured."""
    if not _HAS_GENAI or not GEMINI_API_KEY:
        return ""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        system_instruction = (
            "You are JARVIS, an intelligent and polite voice assistant. "
            "Give concise, conversational responses suitable to be spoken aloud. "
            "Keep answers within 1 to 3 sentences."
        )
        for model_name in ["gemini-flash-latest", "gemini-2.5-flash-lite", "gemini-3.8-flash"]:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"{system_instruction}\nUser: {prompt}"
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as model_err:
                continue
    except Exception as e:
        print(f"Gemini API error: {e}")
    return ""




def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for factual topics and returns a concise 2-sentence summary."""
    clean_query = re.sub(r'^(who is|what is|tell me about|search for|define|explain)\s+', '', query, flags=re.IGNORECASE).strip()
    clean_query = re.sub(r'\b(on wikipedia|in wikipedia)\b', '', clean_query, flags=re.IGNORECASE).strip()
    
    if not clean_query:
        return ""

    try:
        results = wikipedia.search(clean_query)
        if results and len(results) > 0:
            summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False)
            # Remove parenthetical pronunciation guides and clean text
            summary = re.sub(r'\([^)]*\)', '', summary)
            summary = re.sub(r'\s+', ' ', summary).strip()
            # Clean non-ascii characters for clean TTS
            clean_summary = summary.encode('ascii', 'ignore').decode('ascii')
            return f"According to Wikipedia: {clean_summary}"
    except Exception as e:
        print(f"Wikipedia lookup error for '{clean_query}': {e}")
    return ""


def process_assistant_query(query: str) -> str:
    """
    Main conversational brain for Jarvis.
    Handles greetings, small talk, time, date, volume controls, jokes, Wikipedia, and AI LLM.
    """
    q = query.lower().strip()

    # 1. Greetings
    if re.search(r'^(hi|hello|hey|hola|greetings|namaste)\b', q) or q in ["hi", "hello", "hey"]:
        return random.choice(GREETING_RESPONSES)

    if "good morning" in q:
        return "Good morning, sir! I hope you have a productive day ahead."
    if "good afternoon" in q:
        return "Good afternoon, sir! How may I be of service?"
    if "good evening" in q:
        return "Good evening, sir! How has your day been?"
    if "good night" in q:
        return "Good night, sir! Sleep well."

    # 2. Identity and creator
    if any(phrase in q for phrase in ["who are you", "what is your name", "what's your name"]):
        return random.choice(IDENTITY_RESPONSES)

    if any(phrase in q for phrase in ["who created you", "who made you", "who is your creator"]):
        return f"I was created to be your intelligent desktop assistant, inspired by Tony Stark's JARVIS."

    # 3. Status
    if any(phrase in q for phrase in ["how are you", "how are you doing", "are you there", "are you okay"]):
        return random.choice(STATUS_RESPONSES)

    if any(phrase in q for phrase in ["thank you", "thanks", "appreciate it"]):
        return "You're very welcome, sir!"

    # 4. Time and Date
    if any(phrase in q for phrase in ["what time is it", "tell me the time", "current time", "what is the time"]):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."

    if any(phrase in q for phrase in ["what is the date", "today's date", "what day is today", "current date"]):
        now = datetime.datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')}."

    # 5. Jokes
    if any(phrase in q for phrase in ["tell me a joke", "say a joke", "make me laugh"]):
        return random.choice(JOKES)

    # 6. System Volume Control
    if "volume up" in q or "increase volume" in q:
        for _ in range(5):
            pyautogui.press("volumeup")
        return "Volume increased, sir."

    if "volume down" in q or "decrease volume" in q:
        for _ in range(5):
            pyautogui.press("volumedown")
        return "Volume decreased, sir."

    if "mute" in q or "unmute" in q:
        pyautogui.press("volumemute")
        return "Volume toggled."

    # 7. Capabilities & Help
    if any(phrase in q for phrase in ["what can you do", "help me", "commands", "features"]):
        return (
            "I can open applications and websites, play songs on YouTube, "
            "send WhatsApp messages or make calls, answer factual questions via Wikipedia, "
            "adjust system volume, tell jokes, and report the current time."
        )

    # 8. Google Gemini AI (if API key is configured)
    if GEMINI_API_KEY:
        gemini_answer = ask_gemini(query)
        if gemini_answer:
            return gemini_answer

    # 9. Wikipedia queries (for factual searches or when offline)
    wiki_answer = search_wikipedia(q)
    if wiki_answer:
        return wiki_answer

    # 10. Final polite fallback
    return (
        f"I heard you say: {query}. "
        "You can ask me to open apps, play songs on YouTube, send WhatsApp messages, "
        "search Wikipedia, or ask for the time and jokes."
    )

