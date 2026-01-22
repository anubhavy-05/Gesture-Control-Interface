# 📖 AI Virtual Mouse - Complete Instructions

This document provides detailed step-by-step instructions for using the AI Virtual Mouse application.

---

## 📑 Table of Contents

1. [Getting Started](#getting-started)
2. [Opening the Webcam](#opening-the-webcam)
3. [Stopping the Webcam](#stopping-the-webcam)
4. [Using Mouse Controls](#using-mouse-controls)
5. [Opening the Virtual Keyboard](#opening-the-virtual-keyboard)
6. [Hiding the Virtual Keyboard](#hiding-the-virtual-keyboard)
7. [Typing with the Virtual Keyboard](#typing-with-the-virtual-keyboard)
8. [Gesture Controls Reference](#gesture-controls-reference)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [Troubleshooting](#troubleshooting)

---

## **Getting Started**

### **Prerequisites**
Before running the application, ensure you have:
- ✅ Python 3.7+ installed
- ✅ All required packages installed (`pip install -r requirements.txt`)
- ✅ A working webcam connected to your computer
- ✅ Webcam permissions enabled for Python applications

### **Launch the Application**
1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd Gesture-Control-Interface
   ```
3. Run the main script:
   ```bash
   python main.py
   ```

### **Initial Setup Messages**
You will see initialization messages:
```
==================================================
AI Virtual Mouse - Starting...
==================================================

[1/3] Initializing hand detector...
✓ Hand detector initialized

[2/3] Initializing mouse controller...
✓ Mouse controller initialized (Screen: 1920x1080)

[2.5/3] Initializing virtual keyboard...
✓ Virtual keyboard initialized

[3/3] Opening webcam...
✓ Webcam opened successfully (640x480)

==================================================
READY! Webcam window will open now...
==================================================
```

---

## **Opening the Webcam**

### **Automatic Webcam Activation**
The webcam opens **automatically** when you run the application:
```bash
python main.py
```

### **What Happens When Webcam Opens**
1. A window titled **"AI Virtual Mouse"** appears
2. You see a live video feed from your webcam (mirrored for intuitive control)
3. Your hand is automatically detected with colored landmarks
4. FPS (Frames Per Second) is displayed in the top-left corner
5. Control instructions are shown at the top of the window

### **Webcam Camera Selection**
- The application tries **Camera 0** first (default webcam)
- If Camera 0 fails, it automatically tries **Camera 1**
- If both fail, you'll see an error message with troubleshooting steps

### **Webcam Not Opening?**
If the webcam doesn't open, check:
- ✅ Is your webcam connected and powered on?
- ✅ Is another application using the webcam? (Close Zoom, Teams, Skype, etc.)
- ✅ Do you have webcam permissions enabled?
  - **Windows**: Settings → Privacy → Camera → Allow apps to access camera
  - **macOS**: System Preferences → Security & Privacy → Camera
  - **Linux**: Check device permissions with `ls -l /dev/video*`

---

## **Stopping the Webcam**

### **Method 1: Press 'Q' Key (Recommended)**
1. Make sure the **"AI Virtual Mouse"** window is active (click on it)
2. Press the **`Q`** key on your physical keyboard
3. The application will close gracefully
4. You'll see: `Exiting AI Virtual Mouse...`
5. All resources are released automatically

### **Method 2: Close the Window**
1. Click the **X** button on the "AI Virtual Mouse" window
2. The application will close and release the webcam

### **Method 3: Terminal Interrupt**
1. In the terminal where the application is running
2. Press **`Ctrl + C`** (Windows/Linux) or **`Cmd + C`** (macOS)
3. The application will terminate

### **Verification**
After stopping:
- ✅ The video window closes completely
- ✅ Webcam light turns off (if your camera has an indicator light)
- ✅ Terminal shows `Exiting AI Virtual Mouse...`
- ✅ You can now use the webcam in other applications

---

## **Using Mouse Controls**

### **Moving the Cursor**
1. **Raise your index finger** (keep other fingers down except thumb)
2. Move your hand within the camera frame
3. The cursor follows your index finger tip
4. A **green circle** appears on your fingertip for visual feedback
5. You'll see **"MOVE MODE"** displayed on the screen

**Tips for Smooth Movement:**
- Keep your hand steady
- Move slowly for precise control
- You don't need to reach the camera edges - central area maps to full screen
- Green circle indicates active cursor control

### **Left Click**
1. Keep your **index finger up** (cursor control mode)
2. **Bring your thumb close to your index finger** (within 30 pixels)
3. You'll see **"LEFT CLICK!"** in yellow text
4. Release to stop clicking

**Visual Feedback:**
- Yellow circle appears around fingertip
- Distance display shows: `Index-Thumb: 25px` (example)
- Console shows: `✓ LEFT CLICK! Index-Thumb distance: 25px`

### **Right Click**
1. Raise your **middle finger** (keep index down)
2. **Bring your thumb close to middle finger** (within 30 pixels)
3. You'll see **"RIGHT CLICK!"** in orange text
4. Release to stop clicking

**Visual Feedback:**
- Orange circle appears on middle finger
- Display shows: **"RIGHT CLICK MODE"**
- Distance display shows: `Middle-Thumb: 28px`

### **Double Click**
1. Raise your **index finger** (move mode)
2. **Fold your ring finger** (tip below PIP joint)
3. Keep index finger up
4. A double-click is performed
5. You'll see **"DOUBLE CLICK!"** in magenta

**When to Use:**
- Opening files/folders
- Selecting text/words
- Maximizing windows

### **Scrolling**

**Method 1: Pinky Only (Recommended)**
1. Raise **only your pinky finger** (all others down)
2. Move your hand **up** to scroll up ↑
3. Move your hand **down** to scroll down ↓
4. Display shows: **"SCROLL MODE (Pinky)"**

**Method 2: Open Palm**
1. Raise **all five fingers** (open palm)
2. Move your hand vertically to scroll
3. Display shows: **"SCROLL MODE (Palm)"**

**Visual Feedback:**
- Magenta circle on pinky tip
- **"SCROLLING UP ↑"** or **"SCROLLING DOWN ↓"** text
- Console shows: `✓ SCROLL UP: 2 units (delta: 32px)`

---

## **Opening the Virtual Keyboard**

### **Activate Keyboard Mode**
1. Ensure the **"AI Virtual Mouse"** window is active
2. Press the **`K`** key on your physical keyboard
3. The virtual keyboard appears as a semi-transparent overlay
4. You'll see: **"KEYBOARD MODE (Press 'k' to hide)"** at the bottom

### **What You'll See**
The keyboard displays with:
- **Row 1**: Numbers (1-0)
- **Row 2**: QWERTY
- **Row 3**: ASDF GH JKL
- **Row 4**: ZXCV BNM + BACK (Backspace)
- **Row 5**: SPACE + ENTER
- **Semi-transparent** (60% opacity) - you can see your hand through it
- **Dark gray keys** with white text

### **Keyboard Appears But Not Working?**
Ensure:
- ✅ Your hand is visible to the webcam
- ✅ Index finger is raised
- ✅ You're pointing at the keyboard area (lower portion of screen)

---

## **Hiding the Virtual Keyboard**

### **Toggle Keyboard Off**
1. Make sure the **"AI Virtual Mouse"** window is active
2. Press the **`K`** key again on your physical keyboard
3. The virtual keyboard disappears
4. You return to full-screen mouse control mode

### **Quick Toggle**
- Press `K` → Keyboard appears
- Press `K` again → Keyboard disappears
- Press `K` again → Keyboard reappears
- Continue toggling as needed

**Benefits of Hiding:**
- More screen space for hand detection
- Clearer view of video feed
- Better for mouse-only tasks
- No accidental key presses

---

## **Typing with the Virtual Keyboard**

### **Method 1: Hover Typing (Default - 1 Second)**

1. **Show the keyboard** (press `K`)
2. **Raise your index finger**
3. **Point at a key** you want to type
4. **Hold steady** for 1 second
5. Watch the **progress bar** fill up above the key
6. When it reaches 100%, the key is typed automatically
7. You'll see **"Typed: [KEY]"** at the top of the keyboard

**Progress Indicator:**
```
[████████████████████] 100%
```
- Bar fills from left to right
- Color changes from red to green
- Percentage displayed (0% → 100%)

**Example:**
- Hover over **"H"** → Wait 1 second → Types "h"
- Hover over **"E"** → Wait 1 second → Types "e"
- Hover over **"L"** → Wait 1 second → Types "l"
- Hover over **"L"** → Wait 1 second → Types "l"
- Hover over **"O"** → Wait 1 second → Types "o"
- Result: "hello" is typed

### **Method 2: Click Typing (Instant)**

1. **Show the keyboard** (press `K`)
2. **Raise your index finger**
3. **Point at a key** you want to type
4. **Bring thumb and index finger close** (<30px) - same as left-click gesture
5. The key is typed **instantly** (no waiting)
6. You'll see **"Typed: [KEY]"** at the top of the keyboard

**When to Use Click Typing:**
- Fast typing
- Known key locations
- No need to wait for hover

### **Special Keys**

| Key | Function | How to Type |
|-----|----------|-------------|
| **SPACE** | Space character | Hover/Click on wide SPACE key |
| **ENTER** | New line / Submit | Hover/Click on ENTER key |
| **BACK** | Backspace / Delete | Hover/Click on BACK key |

### **Typing Tips**
- ✅ Keep hand steady while hovering
- ✅ Wait for green key highlight before moving to next key
- ✅ Use click typing for speed
- ✅ Use hover typing for accuracy
- ✅ Text appears in your active application (notepad, browser, etc.)

### **Adjusting Hover Time**
If 1 second is too fast or slow, you can change it:

**In main.py:**
```python
keyboard = VirtualKeyboard(frame_width=640, frame_height=480, hover_threshold=1.5)
```
- `0.5` = Fast (half second)
- `1.0` = Default (one second)
- `2.0` = Slow (two seconds)

---

## **Gesture Controls Reference**

### **Complete Gesture List**

| Gesture | Fingers | Action | Visual Indicator |
|---------|---------|--------|-----------------|
| **Index Only Up** | 👆 Index | Move Cursor | Green circle + "MOVE MODE" |
| **Index + Thumb Pinch** | 👆 + 👍 Close | Left Click | Yellow circle + "LEFT CLICK!" |
| **Middle + Thumb Pinch** | 🖕 + 👍 Close | Right Click | Orange circle + "RIGHT CLICK!" |
| **Ring Folded + Index Up** | 👆 + 💍 Down | Double Click | Magenta "DOUBLE CLICK!" |
| **Pinky Only Up** | 🤙 Pinky Only | Scroll Mode | Magenta circle + "SCROLL MODE" |
| **All Fingers Up** | ✋ Open Palm | Alt Scroll | Magenta + "SCROLL MODE (Palm)" |

### **Finger Status Debug Display**
At the bottom of the screen, you'll see:
```
Thumb: 1 | Index: 1 | Middle: 0 | Ring: 0 | Pinky: 0
```
- `1` = Finger is UP
- `0` = Finger is DOWN

---

## **Keyboard Shortcuts**

### **Application Controls**

| Key | Action | Description |
|-----|--------|-------------|
| **Q** | Quit | Exit the application and close webcam |
| **K** | Toggle Keyboard | Show/Hide virtual keyboard overlay |

**Important Notes:**
- These shortcuts work when the **"AI Virtual Mouse"** window is active
- Click on the window first if keyboard shortcuts aren't working
- Shortcuts use your physical keyboard, not the virtual one

---

## **Troubleshooting**

### **Webcam Issues**

**Problem: Webcam not opening**
- ✅ Close other applications using webcam (Zoom, Teams, Skype)
- ✅ Check webcam connection (unplug and replug USB)
- ✅ Verify permissions in system settings
- ✅ Try running as administrator (Windows)

**Problem: Black screen / No video**
- ✅ Check camera privacy settings
- ✅ Ensure webcam isn't covered
- ✅ Test webcam in another application first

**Problem: Wrong camera is used**
- ✅ Disconnect other webcams temporarily
- ✅ The app tries camera 0, then camera 1

---

### **Hand Detection Issues**

**Problem: Hand not detected**
- ✅ Ensure good lighting (bright, even lighting works best)
- ✅ Position hand within camera frame
- ✅ Keep palm facing camera
- ✅ Avoid busy/cluttered backgrounds
- ✅ Display shows "No hand detected" in red when hand isn't visible

**Problem: Hand detection stutters**
- ✅ Improve lighting
- ✅ Close other heavy applications
- ✅ Move hand slower for better tracking
- ✅ Check FPS display (should be 20+ fps)

---

### **Cursor Control Issues**

**Problem: Cursor is jumpy**
- ✅ Increase smoothing: `MouseController(smoothing_factor=10)` in main.py
- ✅ Keep hand more steady
- ✅ Ensure consistent lighting

**Problem: Cursor too slow**
- ✅ Decrease smoothing: `MouseController(smoothing_factor=5)`
- ✅ Move hand faster

**Problem: Can't reach screen edges**
- ✅ Increase padding values in main.py (already set to 200/150)
- ✅ Move hand within central camera area (designed this way)

**Problem: Cursor too sensitive**
- ✅ Decrease padding values in main.py
- ✅ Current: `padding_left=200, padding_right=200`
- ✅ Try: `padding_left=150, padding_right=150`

---

### **Click Detection Issues**

**Problem: Clicks not registering**
- ✅ Bring fingers closer (threshold is 30px)
- ✅ Check distance display: `Index-Thumb: XXpx`
- ✅ Ensure both fingers are visible to camera
- ✅ Try clicking slower

**Problem: Too many accidental clicks**
- ✅ Increase click threshold in main.py: `click_distance_threshold = 40`
- ✅ Keep fingers farther apart during cursor movement

**Problem: Double click not working**
- ✅ Fold ring finger more (tip must be below middle joint)
- ✅ Keep index finger up while folding ring finger

---

### **Scroll Issues**

**Problem: Scroll not activating**
- ✅ Ensure ONLY pinky is up (all other fingers down)
- ✅ Or use open palm (all fingers up)
- ✅ Move hand more vertically (not horizontally)
- ✅ Increase movement amplitude

**Problem: Scroll is jerky**
- ✅ Move hand smoother
- ✅ Adjust `scroll_threshold` in main.py (default: 15)

---

### **Virtual Keyboard Issues**

**Problem: Keyboard not appearing**
- ✅ Press `K` key (not while typing elsewhere)
- ✅ Ensure "AI Virtual Mouse" window is active
- ✅ Check console for error messages

**Problem: Keys not typing**
- ✅ Ensure index finger is up
- ✅ Point directly at key (cursor must be over key area)
- ✅ Wait full hover time (watch progress bar)
- ✅ Or use pinch gesture for instant typing
- ✅ Check typed text appears in an active text editor

**Problem: Wrong keys being typed**
- ✅ Calibrate finger position
- ✅ Keep hand steadier
- ✅ Use click method for precision

**Problem: Typing too slow**
- ✅ Decrease hover time: `VirtualKeyboard(..., hover_threshold=0.5)`
- ✅ Use click typing instead of hover

**Problem: Typing too fast (accidental)**
- ✅ Increase hover time: `VirtualKeyboard(..., hover_threshold=2.0)`
- ✅ Cooldown is set to 0.5s to prevent rapid repeats

---

### **Performance Issues**

**Problem: Low FPS (below 20)**
- ✅ Close other applications
- ✅ Improve lighting (reduces processing load)
- ✅ Use a better webcam
- ✅ Reduce video resolution (already optimized at 640x480)

**Problem: Application crashes**
- ✅ Update Python packages: `pip install --upgrade -r requirements.txt`
- ✅ Check Python version (3.7+ required)
- ✅ Restart computer
- ✅ Check error messages in terminal

---

## **Tips for Best Experience**

### **Lighting**
- ✅ Use bright, even lighting
- ✅ Avoid backlighting (light behind you)
- ✅ Natural daylight works best
- ✅ Avoid shadows on your hand

### **Camera Position**
- ✅ Position camera at chest/face level
- ✅ Keep hand 1-2 feet from camera
- ✅ Center your hand in the frame
- ✅ Avoid tilted camera angles

### **Hand Position**
- ✅ Palm facing camera (not sideways)
- ✅ Keep hand open and spread fingers
- ✅ Avoid overlapping fingers
- ✅ Use clear, distinct gestures

### **Background**
- ✅ Use plain, solid-colored background
- ✅ Avoid cluttered backgrounds
- ✅ Avoid skin-tone colors in background

### **Practice**
- ✅ Practice gestures before real use
- ✅ Start with cursor movement
- ✅ Then try clicking
- ✅ Master keyboard last

---

## **Summary of Key Instructions**

| Task | How To Do It |
|------|-------------|
| **Open Webcam** | Run `python main.py` (automatic) |
| **Stop Webcam** | Press `Q` key or close window |
| **Open Keyboard** | Press `K` key |
| **Hide Keyboard** | Press `K` key again |
| **Move Cursor** | Raise index finger, move hand |
| **Click** | Pinch index and thumb together |
| **Type** | Hover over key for 1 sec OR pinch over key |
| **Scroll** | Raise pinky only, move hand up/down |

---

## **Need More Help?**

- 📚 See [README.md](README.md) for project overview
- 🎮 See [GESTURE_GUIDE.md](GESTURE_GUIDE.md) for gesture details
- ⚙️ See [SMOOTHING_GUIDE.md](SMOOTHING_GUIDE.md) for configuration

---

**Enjoy your hands-free computing experience! 🎉**
