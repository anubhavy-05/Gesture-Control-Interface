# 🎤 Voice Control - Quick Setup

## Installation Instructions

### Install Required Packages

```bash
pip install SpeechRecognition pyaudio
```

### Platform-Specific Instructions

#### **Windows**
If `pyaudio` installation fails, use:
```bash
pip install pipwin
pipwin install pyaudio
```

#### **Linux (Ubuntu/Debian)**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

#### **macOS**
```bash
brew install portaudio
pip install pyaudio
```

## Quick Test

Run the standalone voice controller:
```bash
python voice_control.py
```

## Usage in Main App

1. Run: `python main.py`
2. Press `V` to toggle voice control
3. Speak commands:
   - "Open Chrome"
   - "Type Hello"
   - "Enter"
   - "Show Keyboard"

See **VOICE_CONTROL_GUIDE.md** for complete documentation.
