# 🖐️ AI Virtual Mouse - Gesture Control Interface

A computer vision-based virtual mouse control system that allows you to control your computer using hand gestures captured through a webcam. Control your cursor, click, scroll, and even type on a virtual keyboard - all without touching your mouse or keyboard!

## ✨ Features

### 🖱️ Mouse Control
- **Cursor Movement**: Move your index finger to control the cursor
- **Left Click**: Bring index finger and thumb close together (<30px)
- **Right Click**: Bring middle finger and thumb close together (<30px)
- **Double Click**: Fold your ring finger while index finger is up
- **Scroll**: Use pinky finger only or open palm gesture and move hand up/down

### ⌨️ Virtual Keyboard
- **QWERTY Layout**: Full keyboard with numbers, letters, and special keys
- **Semi-Transparent Overlay**: 60% opacity so you can see your hand and video feed
- **Hover Typing**: Hover over a key for 1 second to type
- **Click Typing**: Pinch thumb and index finger over a key for instant typing
- **Visual Feedback**: Progress bars and typed key display
- **Special Keys**: SPACE, ENTER, BACKSPACE support

### 🎤 Voice Control
- **Open Applications**: Say "Open Chrome", "Open Notepad", "Open Calculator"
- **Type Text**: Say "Type [your text]" to type anything
- **Keyboard Actions**: Say "Enter", "Backspace", "Escape", "Space", "Tab"
- **Keyboard Control**: Say "Show Keyboard" or "Hide Keyboard"
- **Background Threading**: Runs independently without affecting video performance
- **No Video Lag**: Voice recognition in separate thread maintains 25-30 FPS

### 🎯 Advanced Features
- **Settings GUI**: Real-time control panel with sliders to adjust:
  - Smoothing Factor (1-20): Control cursor jitter and responsiveness
  - Mouse Sensitivity (50-300px): Adjust frame reduction margin for screen edge reachability
  - Changes apply instantly without restarting the application!
- **Enhanced Visual Feedback**: 
  - Green circle in cursor move mode
  - **RED circle + "CLICKED!" text** when click happens (0.5s duration)
  - **Futuristic cyan border** showing active detection area with corner decorations
  - Real-time settings display on screen
- **Smooth Cursor Movement**: Advanced smoothing algorithms prevent jitter
- **Frame Reduction Mapping**: Central camera area maps to full screen (no need to reach edges)
- **Real-time FPS Display**: Monitor performance
- **Hand Detection Status**: Visual feedback when hand is detected
- **Cooldown Protection**: Prevents accidental repeated clicks/typing

## 📋 Requirements

- Python 3.7 or higher
- Webcam/Camera
- Windows/Linux/macOS

## 🔧 Installation

1. **Clone the repository** (or download the files):
   ```bash
   cd Gesture-Control-Interface
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - opencv-python
   - mediapipe
   - pyautogui
   - numpy
   - SpeechRecognition (for voice control)
   - pyaudio (for microphone access)

   **Note**: If `pyaudio` installation fails on Windows:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

3. **Verify installation**:
   ```bash
   python main.py
   ```

## 🚀 Quick Start

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Position your hand** in front of the webcam (within the camera frame)

3. **Use gestures** to control your computer:
   - Point with index finger to move cursor
   - Pinch index and thumb to left-click
   - Press `k` to show/hide virtual keyboard
   - Press `v` to toggle voice control

4. **Use voice commands** (after pressing `v`):
   - "Open Chrome"
   - "Type Hello World"
   - "Enter"
   - "Show Keyboard"

5. **Exit**: Press `q` to quit the application

## 📚 Detailed Instructions

For complete step-by-step instructions, gesture guide, and troubleshooting, see **[INSTRUCTIONS.md](INSTRUCTIONS.md)**

## 🎮 Gesture Reference

| Gesture | Action | How to Perform |
|---------|--------|----------------|
| Index Finger Up | Move Cursor | Raise only your index finger |
| Index + Thumb Pinch | Left Click | Bring index and thumb within 30px |
| Middle + Thumb Pinch | Right Click | Bring middle finger and thumb within 30px |
| Ring Finger Folded | Double Click | Fold ring finger while index is up |
| Pinky Only Up | Scroll Mode | Raise only pinky, move hand up/down |
| All Fingers Up | Alt Scroll | Open palm, move hand up/down |

## 🎤 Voice Commands Reference

| Command | Action | Examples |
|---------|--------|----------|
| Open [App] | Open application | "Open Chrome", "Open Notepad", "Open Calculator" |
| Type [Text] | Type text | "Type Hello", "Type example@email.com" |
| Enter | Press Enter key | "Enter", "Return" |
| Backspace | Press Backspace | "Backspace", "Delete", "Back Space" |
| Escape | Press Escape key | "Escape", "Cancel" |
| Space | Press Space key | "Space", "Spacebar" |
| Tab | Press Tab key | "Tab" |
| Show Keyboard | Show virtual keyboard | "Show Keyboard", "Open Keyboard" |
| Hide Keyboard | Hide virtual keyboard | "Hide Keyboard", "Close Keyboard" |
| Stop Listening | Stop voice control | "Stop Listening", "Stop Voice" |
## 📁 Project Structure

```
Gesture-Control-Interface/
│
├── main.py                    # Main application entry point
├── hand_tracker.py            # Hand detection and tracking module
├── mouse_controller.py        # Mouse control and coordinate mapping
├── virtual_keyboard.py        # Virtual keyboard overlay and typing
├── voice_control.py           # Voice command recognition (threaded)
├── settings_gui.py            # Settings GUI with real-time sliders (NEW!)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation (this file)
├── INSTRUCTIONS.md           # Detailed user instructions
├── GESTURE_GUIDE.md          # Gesture reference guide
├── SMOOTHING_GUIDE.md        # Smoothing configuration guide
├── SETTINGS_GUI_GUIDE.md     # Settings GUI usage and tips (NEW!)
├── VOICE_CONTROL_GUIDE.md    # Voice control technical documentation
└── VOICE_SETUP.md            # Voice control quick setup
```

## ⚙️ Configuration

### Adjust Hover Time for Virtual Keyboard
In `main.py`, modify the keyboard initialization:
```python
keyboard = VirtualKeyboard(frame_width=640, frame_height=480, hover_threshold=1.0)
```
- `hover_threshold=0.5` → Faster (0.5 seconds)
- `hover_threshold=2.0` → Slower (2 seconds)

### Adjust Cursor Sensitivity
In `main.py`, modify the padding values:
```python
padding_left = 200    # Increase for more sensitivity
padding_right = 200   # Decrease for less sensitivity
padding_top = 150
padding_bottom = 150
```

### Adjust Smoothing
**Now easier with Settings GUI!** 🎛️

When you run the application, a Settings window will automatically open with sliders to adjust:
- **Smoothing Factor** (1-20): Control cursor jitter and responsiveness
- **Mouse Sensitivity** (50-300px): Adjust screen edge reachability

Changes apply **instantly in real-time** - no restart needed!

For detailed usage, see **[SETTINGS_GUI_GUIDE.md](SETTINGS_GUI_GUIDE.md)**

**Or manually in code:**
In `main.py`, modify the mouse controller:
```python
mouse = MouseController(smoothing_factor=7)  # Higher = smoother but slower
```

## 🐛 Troubleshooting

### Webcam Issues
- **Webcam not opening**: Check if another application is using the camera
- **Black screen**: Verify webcam permissions in system settings
- **Wrong camera**: The app tries camera 0, then camera 1 automatically

### Performance Issues
- **Low FPS**: Close other applications, ensure good lighting
- **Cursor jumpy**: Increase `smoothing_factor` in MouseController
- **Delayed response**: Decrease `smoothing_factor` for faster response

### Gesture Detection
- **Gestures not working**: Ensure good lighting and hand is clearly visible
- **False clicks**: Adjust `click_distance_threshold` in main.py
- **Scroll not working**: Use only pinky finger, move hand more vertically

### Voice Control Issues
- **Voice not available**: Install dependencies: `pip install SpeechRecognition pyaudio`
- **Microphone not detected**: Check microphone permissions in system settings
- **Commands not recognized**: Speak clearly, ensure good internet connection (uses Google API)
- **PyAudio installation fails**: Use `pip install pipwin` then `pipwin install pyaudio` (Windows)
- See [VOICE_CONTROL_GUIDE.md](VOICE_CONTROL_GUIDE.md) for detailed troubleshooting
## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open-source and available for educational and personal use.

## 👨‍💻 Author

Developed with ❤️ using Python, OpenCV, MediaPipe, and PyAutoGUI

## 🙏 Acknowledgments

- **MediaPipe**: Google's hand tracking solution
- **OpenCV**: Computer vision library
- **PyAutoGUI**: Cross-platform GUI automation

## 📞 Support

For issues, questions, or suggestions, please refer to:
- **[INSTRUCTIONS.md](INSTRUCTIONS.md)** - Detailed usage guide
- **[GESTURE_GUIDE.md](GESTURE_GUIDE.md)** - Gesture reference
- **[VOICE_CONTROL_GUIDE.md](VOICE_CONTROL_GUIDE.md)** - Voice control technical guide
- **[VOICE_SETUP.md](VOICE_SETUP.md)** - Quick voice setup instructions

---

**Note**: This application requires appropriate webcam permissions and may need firewall/antivirus exceptions for mouse control functionality.

**Enjoy hands-free computing! 🎉**


**Happy Gesture Controlling! 🖱️👋**

