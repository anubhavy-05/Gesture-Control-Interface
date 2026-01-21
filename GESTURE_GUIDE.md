# Gesture Control Guide

## Hand Gestures for Virtual Mouse

### 🖱️ Mouse Movement

#### **Move Cursor**
- **Gesture**: Index finger up (alone)
- **Action**: Moves the mouse cursor
- **Visual**: Green circle on index fingertip
- **Details**: Cursor follows your index finger with smooth interpolation

---

### 🖱️ Click Actions

#### **Left Click**
- **Gesture**: Bring Index finger tip and Thumb tip close together
- **Threshold**: Less than 30 pixels apart
- **When**: While index finger is up in move mode
- **Visual**: Cyan circle and "LEFT CLICK!" text
- **Use Cases**: 
  - Select files/folders
  - Click buttons
  - Open applications
  - Select text

#### **Right Click**
- **Gesture**: Bring Middle finger tip and Thumb tip close together  
- **Threshold**: Less than 30 pixels apart
- **When**: While middle finger is up
- **Visual**: Orange circle on middle finger, blue "RIGHT CLICK!" text
- **Use Cases**:
  - Context menus
  - File properties
  - Right-click options
  - Copy/Paste menus

#### **Double Click**
- **Gesture**: Fold Ring finger down (ring fingertip below PIP joint)
- **When**: While index finger is up
- **Visual**: Magenta "DOUBLE CLICK!" text at center
- **Use Cases**:
  - Open files/folders
  - Select words
  - Execute applications
  - Full-screen toggle

---

## MediaPipe Hand Landmarks Used

### Key Landmark Points:
- **Landmark 4**: Thumb tip
- **Landmark 8**: Index finger tip
- **Landmark 12**: Middle finger tip
- **Landmark 14**: Ring finger PIP joint (middle joint)
- **Landmark 16**: Ring finger tip

### Distance Calculation:
```python
# Euclidean distance formula
distance = √[(x2 - x1)² + (y2 - y1)²]
```

---

## Technical Implementation

### Left Click Detection
```python
# Calculate distance between index finger and thumb
dist_index_thumb = calculate_distance(index_finger_tip, thumb_tip)

# Trigger click if distance < 30 pixels
if dist_index_thumb < 30:
    mouse.click(button='left')
```

### Right Click Detection
```python
# Calculate distance between middle finger and thumb
dist_middle_thumb = calculate_distance(middle_finger_tip, thumb_tip)

# Trigger right click if distance < 30 pixels
if dist_middle_thumb < 30:
    mouse.click(button='right')
```

### Double Click Detection
```python
# Check if ring finger is folded
# Ring finger is folded when tip (y) > PIP joint (y)
ring_finger_folded = ring_finger_tip[2] > ring_finger_pip[2]

# Trigger double click
if ring_finger_folded and index_up:
    mouse.doubleClick()
```

---

## Cooldown System

### Why Cooldown?
Prevents multiple accidental clicks from a single gesture.

### Current Settings:
- **Cooldown Time**: 0.5 seconds (500ms)
- **Separate Cooldowns**: Each click type has its own cooldown
  - Left Click cooldown
  - Right Click cooldown
  - Double Click cooldown

### Adjusting Cooldown:
In [main.py](main.py), modify:
```python
click_cooldown_time = 0.5  # Change to your preferred value (in seconds)
```

**Recommendations:**
- **Faster**: 0.3 seconds (more responsive, risk of double-triggers)
- **Default**: 0.5 seconds (balanced)
- **Safer**: 0.7 seconds (slower, prevents accidental clicks)

---

## Distance Threshold

### Current Setting:
```python
click_distance_threshold = 30  # pixels
```

### Adjusting Threshold:

**Smaller Threshold (20-25px):**
- ✅ More precise control
- ✅ Prevents accidental clicks
- ❌ Harder to trigger
- ❌ Requires more accuracy

**Default Threshold (30px):**
- ✅ Balanced ease and accuracy
- ✅ Recommended for most users

**Larger Threshold (35-40px):**
- ✅ Easier to trigger
- ✅ Good for larger hand movements
- ❌ May trigger accidentally
- ❌ Less precise

---

## Visual Feedback

### On-Screen Indicators:

| Mode | Color | Display |
|------|-------|---------|
| Move Mode | Green | "MOVE MODE" + green circle |
| Right Click Mode | Orange | "RIGHT CLICK MODE" + orange circle |
| Left Click | Cyan | "LEFT CLICK!" + cyan ring |
| Right Click | Blue | "RIGHT CLICK!" + blue ring |
| Double Click | Magenta | "DOUBLE CLICK!" (center screen) |

### Debug Information:
- FPS counter (top-left)
- Finger states (bottom)
- Distance measurements (when active)

---

## Tips for Best Performance

### 1. **Lighting**
- Use good lighting
- Avoid backlighting
- Ensure hand is well-lit

### 2. **Background**
- Plain, contrasting background works best
- Avoid busy/cluttered backgrounds

### 3. **Camera Position**
- Place camera at comfortable height
- Maintain consistent distance (arm's length)
- Keep hand in frame center

### 4. **Hand Position**
- Keep hand steady for move mode
- Clear, deliberate gestures for clicks
- Don't rush - let cooldown complete

### 5. **Finger Placement**
- Touch thumb to fingertip (not side)
- Make deliberate "pinch" motion
- Clear folding for ring finger

---

## Troubleshooting

### Problem: Clicks triggering too easily
**Solution**: Decrease `click_distance_threshold` to 20-25

### Problem: Hard to trigger clicks
**Solution**: Increase `click_distance_threshold` to 35-40

### Problem: Multiple clicks per gesture
**Solution**: Increase `click_cooldown_time` to 0.7

### Problem: Slow response
**Solution**: Decrease `click_cooldown_time` to 0.3

### Problem: Cursor too jittery
**Solution**: Increase smoothing (see [SMOOTHING_GUIDE.md](SMOOTHING_GUIDE.md))

### Problem: Hand not detected
**Solution**: 
- Check lighting
- Ensure hand is in frame
- Try adjusting camera angle
- Restart application

---

## Keyboard Shortcuts

- **'q'**: Quit application
- **Move mouse to corner**: Emergency stop (PyAutoGUI failsafe)

---

## Code Files

- **[main.py](main.py)**: Main application loop and gesture detection
- **[hand_tracker.py](hand_tracker.py)**: MediaPipe hand tracking
- **[mouse_controller.py](mouse_controller.py)**: Mouse control with PyAutoGUI
- **[SMOOTHING_GUIDE.md](SMOOTHING_GUIDE.md)**: Cursor smoothing configuration

---

## Requirements

```
opencv-python==4.10.0.84
mediapipe==0.10.8
pyautogui==0.9.54
numpy==1.26.3
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python main.py
```

Watch the terminal for click confirmations and the video window for visual feedback!
