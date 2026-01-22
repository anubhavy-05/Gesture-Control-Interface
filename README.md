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

### 🎯 Advanced Features
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

4. **Exit**: Press `q` to quit the application

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
