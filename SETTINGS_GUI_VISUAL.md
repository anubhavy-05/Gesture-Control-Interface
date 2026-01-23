# Settings GUI Visual Layout

```
┌─────────────────────────────────────────────────┐
│  🖱️ Virtual Mouse Settings                  [×]│
├─────────────────────────────────────────────────┤
│                                                 │
│  Smoothing Factor (Jitter Control)             │
│  Higher = Smoother but slower cursor movement  │
│                                                 │
│  ├────○──────────────────────────────────────┤ │
│  1                    10                    20  │
│                  Current: 7                     │
│                                                 │
│ ─────────────────────────────────────────────  │
│                                                 │
│  Mouse Sensitivity (Frame Margin)              │
│  Lower = Easier edges, Higher = More precise   │
│                                                 │
│  ├──────────○────────────────────────────────┤ │
│  50                  150                   300  │
│                 Current: 150px                  │
│                                                 │
│ ─────────────────────────────────────────────  │
│                                                 │
│           ┌─────────────────────┐              │
│           │ Reset to Defaults   │              │
│           └─────────────────────┘              │
│                                                 │
└─────────────────────────────────────────────────┘

Window Size: 400x300 pixels
Always on top: Yes
Resizable: No
```

## Control Layout Details

### Title Bar
- Text: "Virtual Mouse Settings"
- Font: System default
- Close button: Stops GUI thread

### Smoothing Factor Section (Row 1-4)
```
┌─────────────────────────────────────────────────┐
│ Smoothing Factor (Jitter Control)           ◄── Bold Label
│ Higher = Smoother but slower cursor movement ◄── Description (Gray)
│                                                 
│ ├────○──────────────────────────────────────┤  ◄── Slider
│ 1     5     10    15    20                   ◄── Tick Marks
│           Current: 7                         ◄── Value Label
└─────────────────────────────────────────────────┘
```

### Mouse Sensitivity Section (Row 5-8)
```
┌─────────────────────────────────────────────────┐
│ Mouse Sensitivity (Frame Margin)            ◄── Bold Label
│ Lower = Easier edges, Higher = More precise ◄── Description (Gray)
│                                                 
│ ├──────────○────────────────────────────────┤  ◄── Slider
│ 50    100   150   200   250   300           ◄── Tick Marks
│          Current: 150px                      ◄── Value Label
└─────────────────────────────────────────────────┘
```

### Reset Button (Row 9)
```
┌─────────────────────────────────────────────────┐
│           ┌─────────────────────┐              
│           │ Reset to Defaults   │               ◄── Button (Centered)
│           └─────────────────────┘              
└─────────────────────────────────────────────────┘
```

## Slider Behavior

### Smoothing Factor Slider
- **Range**: 1 to 20
- **Step**: 1 (integer values only)
- **Tick Interval**: Every 5 units (1, 5, 10, 15, 20)
- **Length**: 300 pixels
- **Orientation**: Horizontal
- **Default Position**: 7

### Mouse Sensitivity Slider
- **Range**: 50 to 300
- **Step**: 10 (multiples of 10)
- **Tick Interval**: Every 50 units (50, 100, 150, 200, 250, 300)
- **Length**: 300 pixels
- **Orientation**: Horizontal
- **Default Position**: 150

## Color Scheme

```
Background: White/Light Gray (System Default)
Text:
  - Labels: Black (Bold)
  - Descriptions: Dark Gray
  - Values: Black
Slider:
  - Track: Gray
  - Thumb: System accent color (blue on Windows)
  - Ticks: Gray
Button:
  - Background: System default
  - Text: Black
  - Hover: Lighter shade
```

## Font Specifications

- **Title**: Arial 14pt Bold
- **Labels**: Arial 10pt Bold
- **Descriptions**: Arial 8pt Regular
- **Values**: Arial 9pt Regular
- **Button**: System default

## Spacing and Padding

```
Window Padding: 20px on all sides
Between Sections: 20px vertical spacing
Label to Description: 5px
Description to Slider: 5px
Slider to Value: 10px
Value to Next Section: 20px
```

## Interactive Elements

### Sliders
- **On Drag**: Updates value label immediately
- **On Change**: Prints to console and updates shared variable
- **Visual**: Smooth sliding animation

### Reset Button
- **On Click**: 
  - Smoothing → 7
  - Sensitivity → 150
  - Updates sliders visually
  - Prints "All settings reset to defaults" to console

### Close Button (X)
- **On Click**: 
  - Prints "Settings window closed"
  - Sets `is_running = False`
  - Destroys window
  - Exits GUI thread

## Window Behavior

- **Always On Top**: Yes (stays above other windows)
- **Resizable**: No (fixed 400x300)
- **Position**: System decides (typically center-screen)
- **Focus**: Does not steal focus from OpenCV window
- **Minimize**: Can be minimized to taskbar

## Thread Integration

```
┌─────────────────────────────────────────────────┐
│         Settings GUI (Tkinter Thread)          │
├─────────────────────────────────────────────────┤
│                                                 │
│  User moves slider                              │
│         │                                       │
│         ▼                                       │
│  update_smoothing() callback                    │
│         │                                       │
│         ▼                                       │
│  self.smoothing_factor = new_value              │
│         │                                       │
│         ▼                                       │
│  Print to console                               │
│                                                 │
└─────────────────────────────────────────────────┘
         │
         │ (Shared Variable)
         │
         ▼
┌─────────────────────────────────────────────────┐
│        Main Script (OpenCV Thread)              │
├─────────────────────────────────────────────────┤
│                                                 │
│  In cursor movement loop:                       │
│         │                                       │
│         ▼                                       │
│  value = settings_gui.get_smoothing_factor()    │
│         │                                       │
│         ▼                                       │
│  mouse.smoothing_factor = value                 │
│         │                                       │
│         ▼                                       │
│  Cursor moves with new smoothing                │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Console Output Examples

### On Slider Movement:
```
[Settings] Smoothing factor updated to: 10
[Settings] Mouse sensitivity (padding) updated to: 120px
```

### On Reset:
```
[Settings] All settings reset to defaults
```

### On Window Close:
```
[Settings] Settings window closed
```

### On Startup:
```
[2.25/3] Initializing settings GUI...
[Settings] Settings GUI started in separate thread
✓ Settings GUI initialized
  Note: Settings window will appear alongside the camera view
```

## Platform-Specific Notes

### Windows
- Native Windows theme
- Blue accent color for sliders
- Smooth animations

### macOS
- Aqua theme
- System accent color
- Slight visual differences

### Linux
- GTK or Qt theme (depends on tkinter backend)
- May look slightly different
- Functionality identical

---

This is a text-based representation of the GUI. The actual window will render with your system's native widgets and theme!
