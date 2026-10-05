# 🤖 JARVIS - AI Desktop Voice Assistant

[![Python Version](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![UI Framework](https://img.shields.io/badge/UI-Eel%20%2B%20HTML5%2FCSS3-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://github.com/python-eel/Eel)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An intelligent, futuristic desktop voice assistant built with **Python** and **Eel**. JARVIS features an interactive web-based UI with 3D canvas particle animations, voice visualizers, offline Text-to-Speech (TTS), speech recognition, application launcher, YouTube playback, and automated WhatsApp calling/messaging.

---

## 📌 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Requirements](#-system-requirements)
- [Quick Start Installation](#-quick-start-installation)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
  - [Step 3: Activate the Virtual Environment](#step-3-activate-the-virtual-environment)
  - [Step 4: Install Dependencies](#step-4-install-dependencies)
- [Running the Project](#-running-the-project)
  - [Option A: Running in Visual Studio Code (Recommended)](#option-a-running-in-visual-studio-code-recommended)
  - [Option B: Running via Terminal](#option-b-running-via-terminal)
- [Voice & Chat Commands](#-voice--chat-commands)
- [Project Architecture](#-project-architecture)
- [Configuration & Customization](#-configuration--customization)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **Futuristic Holographic UI**:
  - Rotating 3D particle sphere animated in HTML5 Canvas.
  - Dynamic Siri-style waveform voice visualizer (`SiriWave.js`).
  - Animated typography and transitions (`Textillate.js`).
- **Dual Interaction Modes**:
  - **Voice Mode**: Click the microphone icon or press `Win + J` to speak.
  - **Text Mode**: Type directly in the chat box and hit Enter or Send.
- **Speech Recognition & Voice Synthesis**:
  - Speech-to-Text via Google Speech Recognition API (`SpeechRecognition`).
  - Text-to-Speech voice responses using Windows SAPI5 (`pyttsx3`).
- **Application & Website Launcher**:
  - Open desktop apps (Android Studio, OneNote, etc.) from local SQLite registry.
  - Open websites (YouTube, Spotify, OpenAI, Canva, etc.) automatically in your browser.
- **Media Controls**:
  - Search and instantly stream music/videos on YouTube with natural language.
- **WhatsApp Automation**:
  - Integrates with your SQLite contact database to search contacts and automate sending WhatsApp messages, voice calls, or video calls via `pyautogui`.
- **Multiprocessing**:
  - Separate background process support for hands-free wake-word hotword detection (`pvporcupine`).

---

## 🛠️ Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11, Eel, Multiprocessing, SQLite3 |
| **Audio & Speech** | SpeechRecognition, PyAudio, pyttsx3, playsound |
| **Automation** | PyAutoGUI, pywhatkit, webbrowser, subprocess |
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5, jQuery |
| **Animations** | SiriWave.js, Modernizr, Textillate.js, Animate.css |

---

## 💻 System Requirements

- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **Python**: **Python 3.11** *(Highly recommended: Python 3.11 provides pre-built binary wheels for `PyAudio` on Windows, avoiding C++ build tools requirements)*
- **Microphone**: Working microphone and sound output
- **Browser**: Microsoft Edge or Google Chrome (used in app mode)
- **Internet Connection**: Required for speech recognition and YouTube streaming

---

## 🚀 Quick Start Installation

Follow these steps to clone and run JARVIS on your local machine:

### Step 1: Clone the Repository

Open your terminal (PowerShell or Command Prompt) and run:

```bash
git clone https://github.com/<your-username>/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

---

### Step 2: Create a Virtual Environment

It is strongly recommended to use a virtual environment with **Python 3.11**:

```powershell
py -3.11 -m venv .venv
```

> **Note:** If Python 3.11 is your primary system Python, you can simply run:
> ```powershell
> python -m venv .venv
> ```

---

### Step 3: Activate the Virtual Environment

- **In PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(If you encounter an execution policy error in PowerShell, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, then re-run the activate command).*

- **In Command Prompt (cmd.exe):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

- **In Git Bash:**
  ```bash
  source .venv/Scripts/activate
  ```

---

### Step 4: Install Dependencies

With the virtual environment activated, upgrade pip and install the required packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Option A: Running in Visual Studio Code (Recommended)

1. Open the project folder in **Visual Studio Code**:
   ```bash
   code .
   ```
2. Select the Python interpreter:
   - Press `Ctrl + Shift + P`
   - Type `Python: Select Interpreter`
   - Choose: `Python 3.11.x ('.venv': venv) .\.venv\Scripts\python.exe`
3. Launch JARVIS:
   - Press **`F5`** (or go to the **Run and Debug** tab `Ctrl + Shift + D` and click **Run Jarvis Assistant (run.py)**).
4. JARVIS will start:
   - Startup audio will play.
   - An application window will open displaying the animated interface.

---

### Option B: Running via Terminal

Make sure your virtual environment is activated (`(.venv)` should appear in your terminal prompt):

- **Full Assistant (GUI + Background Hotword Listener):**
  ```powershell
  python run.py
  ```

- **GUI Assistant Only:**
  ```powershell
  python main.py
  ```

---

## 🗣️ Voice & Chat Commands

You can interact with JARVIS by clicking the **Microphone** button, pressing `Win + J`, or typing in the text box:

| Action | Example Command | Notes |
| :--- | :--- | :--- |
| **Launch Desktop App** | `"open android studio"`, `"open one note"` | Launches local app registered in database |
| **Open Website** | `"open youtube"`, `"open spotify"`, `"open openai"` | Opens web app in default browser |
| **YouTube Playback** | `"play believer on youtube"`, `"play lofi hip hop on youtube"` | Searches and auto-plays video on YouTube |
| **WhatsApp Message** | `"send message to [Contact Name]"` | Prompts for message content and sends via WhatsApp |
| **WhatsApp Voice Call** | `"phone call [Contact Name]"` | Triggers WhatsApp voice call |
| **WhatsApp Video Call** | `"video call [Contact Name]"` | Triggers WhatsApp video call |

---

## 📂 Project Architecture

```
jarvis-voice-assistant/
│
├── .vscode/                 # Preconfigured VS Code settings & debug launch configurations
│   ├── launch.json
│   └── settings.json
│
├── engine/                  # Core Python backend modules
│   ├── command.py           # Speech recognition, TTS, and command dispatcher
│   ├── config.py            # Assistant settings & API keys
│   ├── db.py                # SQLite table setup & seed script
│   ├── features.py          # Assistant actions (apps, media, WhatsApp, etc.)
│   └── helper.py            # Text processing and regex helpers
│
├── www/                     # Web UI frontend assets
│   ├── assets/
│   │   ├── audio/           # Sound files (start_sound.mp3)
│   │   ├── img/             # Application icons & graphics
│   │   └── vendore/         # CSS/JS vendor plugins
│   ├── controller.js        # JavaScript UI hooks exposed to Python
│   ├── index.html           # Main UI dashboard layout
│   ├── main.js              # Event listeners & Eel bridge
│   ├── script.js            # 3D interactive particle sphere animation
│   └── style.css            # Custom futuristic UI styling
│
├── contacts.csv             # Contact list data
├── jarvis.db                # SQLite database for contacts and app/web commands
├── main.py                  # Single-process GUI entry point
├── requirements.txt         # Python package dependencies
├── run.py                   # Multi-process entry point (GUI + hotword listener)
└── README.md                # Project documentation
```

---

## ⚙️ Configuration & Customization

### 1. Enable Hands-Free Wake-Word Detection ("Jarvis" / "Alexa")
By default, hotword listening is safely bypassed until an AccessKey is configured:
1. Get a free key from the [Picovoice Console](https://console.picovoice.ai/).
2. Open `engine/config.py` and set your key:
   ```python
   PORCUPINE_ACCESS_KEY = "your_picovoice_access_key_here"
   ```
3. Now saying **"Jarvis"** or **"Alexa"** will automatically trigger the assistant.

### 2. Customize Assistant Name
In `engine/config.py`:
```python
ASSISTANT_NAME = "jarvis"
```

### 3. Add Custom Commands to SQLite Database
You can register your own desktop apps or websites by editing `engine/db.py` or executing SQLite queries on `jarvis.db`:
```python
# Insert a new local app:
cursor.execute("INSERT INTO sys_command VALUES (null, 'calculator', 'calc.exe')")

# Insert a new website:
cursor.execute("INSERT INTO web_command VALUES (null, 'github', 'https://github.com')")
con.commit()
```

---

## ❓ Troubleshooting

#### 1. Error installing `pyaudio` (`fatal error C1083: Cannot open include file: 'portaudio.h'`)
- **Reason**: PyAudio lacks pre-compiled wheels for Python 3.14+ on Windows.
- **Fix**: Use **Python 3.11** for your virtual environment (`py -3.11 -m venv .venv`). Python 3.11 automatically downloads and installs pre-built binary wheels without requiring C++ build tools.

#### 2. Microphone not detecting voice
- Check that Windows microphone permissions are enabled:
  - **Windows Settings** > **Privacy & Security** > **Microphone** > Enable **Let desktop apps access your microphone**.
- Verify that your default recording device is properly set in Windows Sound Settings.

#### 3. Browser does not launch automatically
- Jarvis defaults to opening Microsoft Edge in application mode:
  ```powershell
  start msedge.exe --app="http://localhost:8000/index.html"
  ```
- If Edge is unavailable, you can open Chrome or any browser manually and navigate to:
  ```
  http://localhost:8000/index.html
  ```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">Made with ❤️ for AI & Voice Automation Enthusiasts</p>
