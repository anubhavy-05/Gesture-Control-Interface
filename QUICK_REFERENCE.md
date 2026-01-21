# Quick Reference Card - Virtual Mouse Gestures

## 🎯 Quick Gesture Guide

### 1️⃣ MOVE CURSOR
```
    👆 Index finger UP
    🖐️ Other fingers DOWN
    
    → Cursor follows index finger
    → Green circle indicator
```

### 2️⃣ LEFT CLICK
```
    👆 Index finger UP
    👍 Pinch Index + Thumb together
    📏 Distance < 30 pixels
    
    → Left mouse click
    → Cyan "LEFT CLICK!" indicator
```

### 3️⃣ RIGHT CLICK
```
    🖕 Middle finger UP  
    👍 Pinch Middle + Thumb together
    📏 Distance < 30 pixels
    
    → Right mouse click
    → Orange indicator + Blue "RIGHT CLICK!"
```

### 4️⃣ DOUBLE CLICK
```
    👆 Index finger UP
    💍 Ring finger FOLDED DOWN
    
    → Double click
    → Magenta "DOUBLE CLICK!" (center screen)
```

---

## 📊 MediaPipe Landmark Numbers

```
Hand Skeleton Reference:

         (4) Thumb Tip
           \
            \
        (8) Index Tip ----
       /                  |
      /                   |  < 30px for LEFT CLICK
     /                    |
    |                     |
(12) Middle Tip ----------
    |                     
    |                     |  < 30px for RIGHT CLICK
    |                     |
    |                     
(14) Ring PIP Joint       
    |                     
(16) Ring Tip (folded if below PIP)
    
```

---

## ⚙️ Configuration Variables

### In main.py:

```python
# Distance threshold for clicks (line ~120)
click_distance_threshold = 30  # pixels

# Cooldown between clicks (line ~119)
click_cooldown_time = 0.5  # seconds

# Mouse smoothing (line ~58)
mouse = MouseController(smoothing_factor=7, buffer_size=5)
```

---

## 🎨 Color Codes

| Gesture | Color | RGB |
|---------|-------|-----|
| Move Mode | Green | (0, 255, 0) |
| Right Click Mode | Orange | (255, 165, 0) |
| Left Click | Cyan | (0, 255, 255) |
| Right Click | Blue | (0, 100, 255) |
| Double Click | Magenta | (255, 0, 255) |

---

## 🔧 Tuning Tips

### If clicks are too sensitive:
```python
click_distance_threshold = 20  # Lower = harder to trigger
```

### If clicks are too hard to trigger:
```python
click_distance_threshold = 40  # Higher = easier to trigger
```

### If getting double/triple clicks:
```python
click_cooldown_time = 0.7  # Higher = more delay between clicks
```

### If response is too slow:
```python
click_cooldown_time = 0.3  # Lower = faster response
```

---

## 📝 Code Logic Summary

### Left Click:
```python
# 1. Check index finger is up
if fingers[1] == 1:
    # 2. Calculate distance
    dist = distance(index_tip, thumb_tip)
    # 3. Check threshold
    if dist < 30:
        # 4. Click!
        mouse.click('left')
```

### Right Click:
```python
# 1. Check middle finger is up  
if fingers[2] == 1:
    # 2. Calculate distance
    dist = distance(middle_tip, thumb_tip)
    # 3. Check threshold
    if dist < 30:
        # 4. Right click!
        mouse.click('right')
```

### Double Click:
```python
# 1. Check ring finger position
ring_folded = ring_tip[y] > ring_pip[y]
# 2. Check index is up
if ring_folded and fingers[1] == 1:
    # 3. Double click!
    mouse.doubleClick()
```

---

## 🚀 Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the virtual mouse
python main.py

# Press 'q' to quit
```

---

## 📚 Documentation Files

- [GESTURE_GUIDE.md](GESTURE_GUIDE.md) - Detailed gesture guide
- [SMOOTHING_GUIDE.md](SMOOTHING_GUIDE.md) - Cursor smoothing settings
- [README.md](README.md) - Project overview

---

## ✅ Testing Checklist

- [ ] Left click: Pinch index + thumb
- [ ] Right click: Pinch middle + thumb  
- [ ] Double click: Fold ring finger
- [ ] Cursor moves smoothly with index up
- [ ] No accidental clicks during movement
- [ ] Cooldown prevents multiple clicks
- [ ] Visual feedback appears correctly
- [ ] FPS shows good performance (>20 FPS)

---

## 🐛 Common Issues

**Q: Clicks happening accidentally**
A: Decrease `click_distance_threshold` to 20-25

**Q: Can't trigger clicks**
A: Increase `click_distance_threshold` to 35-40

**Q: Ring finger double-click not working**
A: Ensure ring fingertip is clearly below the PIP joint

**Q: Cursor too shaky**
A: Increase `smoothing_factor` in MouseController

---

Made with ❤️ using Python, OpenCV, MediaPipe, and PyAutoGUI
