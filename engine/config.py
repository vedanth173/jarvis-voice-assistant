import os

ASSISTANT_NAME = "jarvis"

# Picovoice Porcupine AccessKey for wake-word detection (https://console.picovoice.ai/)
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")

# Google Gemini API Key for AI responses (free at https://aistudio.google.com/)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
