import os

ASSISTANT_NAME = "jarvis"

# Picovoice Porcupine AccessKey for hotword detection (get a free key at https://console.picovoice.ai/)
PORCUPINE_ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY", "")