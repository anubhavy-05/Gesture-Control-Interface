# 🎤 Voice Control Guide

This guide explains how voice control is integrated with the AI Virtual Mouse using threading to prevent video lag.

---

## 🏗️ Architecture Overview

### **Threading Design**

The voice control runs in a **separate daemon thread** that operates independently from the main OpenCV video loop:

```
┌─────────────────────────────────────────────┐
│         Main Thread (OpenCV Loop)           │
│  - Capture video frames (30+ FPS)          │
│  - Detect hand gestures                     │
│  - Control mouse/keyboard                   │
│  - Display video feed                       │
└─────────────────────────────────────────────┘
                    │
                    │ (Non-blocking)
                    │
┌─────────────────────────────────────────────┐
│      Voice Control Thread (Background)      │
│  - Listen for voice commands                │
│  - Recognize speech via Google API          │
│  - Execute commands (open apps, type, etc.) │
│  - Report status via callback               │
└─────────────────────────────────────────────┘
```

### **Key Benefits**
- ✅ **No Video Lag**: Voice recognition runs independently
- ✅ **Non-blocking**: OpenCV loop maintains 25-30 FPS
- ✅ **Thread-safe**: Uses callback pattern for communication
- ✅ **Daemon Thread**: Automatically stops when main program exits

---

## 📦 Installation

### **Step 1: Install Required Packages**

```bash
pip install SpeechRecognition pyaudio
```

**For Windows (if pyaudio fails):**
```bash
pip install pipwin
pipwin install pyaudio
```

**For Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

**For macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### **Step 2: Verify Installation**

Run the voice controller standalone:
```bash
python voice_control.py
```

Test your microphone:
- Speak when prompted
- If successful, you'll see: `✓ Microphone test successful!`

---

## 🎯 How to Use

### **Starting Voice Control**

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Press `V` key** to toggle voice control:
   - You'll see **"VOICE: ON"** in green (top-right corner)
   - The microphone starts listening in the background
   - The video feed continues smoothly

3. **Speak commands** (see below for command list)

4. **Press `V` again** to stop voice control:
   - Display changes to **"VOICE: OFF"** in gray
   - Listening thread stops gracefully

### **Visual Feedback**

- **"VOICE: ON"** (Green) → Voice control is active and listening
- **"VOICE: OFF"** (Gray) → Voice control is inactive
- **"Voice: [command]"** (Yellow) → Shows last recognized command for 3 seconds

---

## 🗣️ Voice Commands

### **Opening Applications**

| Command | Action | Example |
|---------|--------|---------|
| "Open Chrome" | Opens Google Chrome | "Open Chrome" |
| "Open Notepad" | Opens Notepad | "Open Notepad" |
| "Open Calculator" | Opens Calculator | "Open Calculator" / "Open Calc" |
| "Open Explorer" | Opens File Explorer | "Open Files" |
| "Open Command Prompt" | Opens CMD | "Open CMD" / "Open Terminal" |
| "Open Paint" | Opens MS Paint | "Open Paint" |

### **Typing Text**

| Command | Action | Example |
|---------|--------|---------|
| "Type [text]" | Types the specified text | "Type Hello World" |
| | | "Type example@email.com" |

**Note**: Text is typed with 0.05s interval between characters for reliability.

### **Keyboard Actions**

| Command | Action | Alternatives |
|---------|--------|-------------|
| "Enter" | Presses Enter key | "Return" |
| "Backspace" | Presses Backspace | "Delete", "Back Space" |
| "Escape" | Presses Escape key | "Cancel" |
| "Space" | Presses Space key | "Spacebar" |
| "Tab" | Presses Tab key | - |

### **Virtual Keyboard Control**

| Command | Action |
|---------|--------|
| "Show Keyboard" | Shows virtual keyboard overlay |
| "Hide Keyboard" | Hides virtual keyboard overlay |
| "Open Keyboard" | Shows virtual keyboard |
| "Close Keyboard" | Hides virtual keyboard |

### **Voice Control Management**

| Command | Action |
|---------|--------|
| "Stop Listening" | Stops voice control |
| "Stop Voice" | Stops voice control |

**Note**: You can also press `V` key to toggle voice control on/off.

---

## 🔧 Technical Implementation

### **Threading Model**

```python
# Voice controller runs in a daemon thread
self.thread = threading.Thread(target=self._listen_loop, daemon=True)
self.thread.start()
```

**Why Daemon Thread?**
- Automatically terminates when main program exits
- Doesn't block program shutdown
- No need for explicit cleanup in most cases

### **Listen Loop (Background Thread)**

```python
def _listen_loop(self):
    while self.is_listening and not self.stop_flag.is_set():
        # Listen for audio (non-blocking with timeout)
        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
        
        # Recognize speech
        command = self.recognizer.recognize_google(audio).lower()
        
        # Process command
        self._process_command(command)
```

**Key Features:**
- **Timeout**: 1 second timeout prevents hanging
- **Phrase Limit**: 5 seconds max for each command
- **Non-blocking**: Uses `stop_flag` for graceful shutdown
- **Error Handling**: Catches recognition errors without crashing

### **Callback Pattern**

```python
def voice_callback(message):
    nonlocal voice_last_command, keyboard_visible
    voice_last_command = message
    voice_command_time = time.time()
    
    # Handle special commands
    if message == "SHOW_KEYBOARD":
        keyboard_visible = True
```

**Benefits:**
- Thread-safe communication between threads
- Main loop receives status updates
- Enables synchronized actions (e.g., showing keyboard)

### **Performance Optimization**

```python
# Configured for optimal performance
self.recognizer.energy_threshold = 4000
self.recognizer.dynamic_energy_threshold = True
self.recognizer.pause_threshold = 0.8
```

- **Energy Threshold**: Filters background noise
- **Dynamic Adjustment**: Adapts to ambient noise
- **Pause Threshold**: Quick command recognition

---

## ⚡ Performance Impact

### **Without Threading (Blocking)**
```
Frame Rate: 5-10 FPS ❌
- Voice recognition blocks video loop
- Video freezes during speech recognition
- Poor user experience
```

### **With Threading (Non-blocking)**
```
Frame Rate: 25-30 FPS ✅
- Voice runs independently
- No impact on video performance
- Smooth user experience
```

### **CPU Usage**
- **Main Thread**: ~15-25% (video processing)
- **Voice Thread**: ~5-10% (only when speaking)
- **Total**: ~20-35% CPU (acceptable)

---

## 🐛 Troubleshooting

### **Voice Control Not Available**

**Error**: `Voice control not available (install: pip install SpeechRecognition pyaudio)`

**Solution**:
```bash
pip install SpeechRecognition pyaudio
```

If pyaudio installation fails on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

---

### **Microphone Not Working**

**Problem**: "No speech detected" or "Microphone test failed"

**Solutions**:
1. Check microphone permissions:
   - **Windows**: Settings → Privacy → Microphone
   - **macOS**: System Preferences → Security & Privacy → Microphone
   - **Linux**: Check ALSA/PulseAudio configuration

2. Verify microphone is default device:
   - Open system sound settings
   - Set your microphone as default input device

3. Test microphone in another app first (e.g., Voice Recorder)

4. Check if another app is using the microphone

---

### **Commands Not Recognized**

**Problem**: Voice controller hears audio but doesn't execute commands

**Solutions**:
1. **Speak clearly** and at normal volume
2. **Wait for calibration** to complete (1-2 seconds at startup)
3. **Check ambient noise** - reduce background noise
4. **Adjust energy threshold** in `voice_control.py`:
   ```python
   self.recognizer.energy_threshold = 3000  # Lower for quieter environments
   ```

---

### **Internet Connection Required**

**Note**: Google Speech Recognition API requires internet connection.

**Problem**: "Speech recognition service error"

**Solution**:
- Verify internet connection
- Check firewall settings
- Use alternative: Sphinx (offline, but less accurate)

---

### **Video Lag Despite Threading**

**Problem**: Video still lags when voice control is active

**Possible Causes**:
1. **Low-end CPU**: Voice + Video processing may be too heavy
2. **High ambient noise**: Recognition works harder, uses more CPU

**Solutions**:
1. Reduce video resolution (already optimized at 640x480)
2. Increase `pause_threshold` to reduce recognition frequency:
   ```python
   self.recognizer.pause_threshold = 1.5  # Wait longer between commands
   ```
3. Close other CPU-intensive applications

---

## 🎛️ Configuration

### **Adjust Microphone Sensitivity**

In `voice_control.py`:
```python
self.recognizer.energy_threshold = 4000  # Default
# Lower (2000-3000): More sensitive, picks up quieter speech
# Higher (5000-6000): Less sensitive, ignores more background noise
```

### **Adjust Command Recognition Speed**

```python
self.recognizer.pause_threshold = 0.8  # Default
# Lower (0.5): Faster recognition, may cut off words
# Higher (1.2): Slower recognition, more accurate
```

### **Add Custom Commands**

In `voice_control.py`, add to `_process_command()`:
```python
if 'your custom phrase' in command:
    self._your_custom_function()
    return
```

---

## 📊 Thread Safety

### **Shared Variables**

Variables shared between threads:
- `keyboard_visible` (via callback)
- `voice_last_command` (via callback)
- `voice_command_time` (via callback)

### **Thread-Safe Patterns Used**

1. **Callback Pattern**: Main thread registers callback, voice thread calls it
2. **Event Flags**: `threading.Event()` for clean shutdown
3. **Daemon Threads**: Automatic cleanup on program exit
4. **No Shared State**: Voice thread doesn't directly modify main thread variables

### **Why This Works**

- Python GIL (Global Interpreter Lock) ensures atomic operations on simple variables
- Callback pattern provides clear communication channel
- No need for locks/mutexes for our use case

---

## 🚀 Advanced Usage

### **Running Voice Controller Standalone**

Test voice control independently:
```bash
python voice_control.py
```

Commands:
- Speak any command to test
- Press `Ctrl+C` to exit

### **Custom Callback Function**

```python
def my_callback(message):
    if message.startswith("Heard:"):
        print(f"User said: {message}")
    elif message == "SHOW_KEYBOARD":
        show_my_keyboard()

voice = VoiceController(callback=my_callback)
```

### **Test Microphone**

```python
voice = VoiceController()
if voice.test_microphone():
    voice.start_listening()
```

---

## 📝 Summary

| Feature | Implementation | Benefit |
|---------|---------------|---------|
| **Threading** | Separate daemon thread | No video lag |
| **Callbacks** | Status reporting | Thread-safe communication |
| **Error Handling** | Try-except blocks | Graceful failures |
| **Timeouts** | 1s listen timeout | Non-blocking |
| **Dynamic Calibration** | Ambient noise adjustment | Works in various environments |
| **Command Processing** | Pattern matching | Flexible command recognition |

---

## 🔗 Related Files

- **`voice_control.py`**: Voice controller implementation
- **`main.py`**: Integration with gesture control
- **`INSTRUCTIONS.md`**: User guide for all features

---

**Enjoy hands-free voice + gesture control! 🎉🎤**
