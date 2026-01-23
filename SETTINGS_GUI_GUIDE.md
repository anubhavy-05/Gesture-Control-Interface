# Settings GUI Guide

## Overview
The **Settings GUI** is a real-time control panel for your Virtual Mouse project. It allows you to adjust key parameters without restarting the application.

## Features

### 1. **Smoothing Factor Slider** (1-20)
- **Purpose**: Controls cursor jitter and movement smoothness
- **How it works**: 
  - Lower values (1-5): Faster, more responsive cursor, but more jittery
  - Medium values (6-10): Balanced smoothness and responsiveness ✓ Recommended
  - Higher values (11-20): Very smooth cursor, but slower to respond
- **Default**: 7
- **Use case**: 
  - Reduce jitter if your hand shakes
  - Increase responsiveness for precise tasks

### 2. **Mouse Sensitivity Slider** (50-300px)
- **Purpose**: Controls the frame reduction margin (screen edge reachability)
- **How it works**:
  - Lower values (50-100): Easier to reach screen edges, less hand movement needed
  - Medium values (100-200): Balanced control ✓ Recommended
  - Higher values (200-300): More precise control, requires more hand movement
- **Default**: 150px
- **Use case**:
  - Lower sensitivity for multi-monitor setups
  - Higher sensitivity for precise drawing/design work

## Usage

### Starting the Settings GUI
The Settings GUI automatically starts when you run `main.py`:

```bash
python main.py
```

You'll see two windows:
1. **OpenCV Camera Window**: Shows your hand tracking
2. **Settings Window**: Small control panel with sliders

### Adjusting Settings in Real-Time

1. **While the virtual mouse is running**, simply drag the sliders in the Settings window
2. Changes apply **immediately** - no need to restart!
3. Watch the OpenCV window to see the current values displayed at the top

### Resetting to Defaults

Click the **"Reset to Defaults"** button in the Settings window to restore:
- Smoothing Factor: 7
- Mouse Sensitivity: 150px

## Tips & Best Practices

### Finding Your Perfect Settings

1. **Start with defaults** (Smoothing: 7, Sensitivity: 150)
2. **Test cursor movement** by raising your index finger
3. **Adjust smoothing** if cursor is too jittery or too slow
4. **Adjust sensitivity** if reaching screen edges is too hard or too easy
5. **Save your preferred values** mentally or write them down

### Common Scenarios

| Scenario | Recommended Settings |
|----------|---------------------|
| Gaming | Smoothing: 4-6, Sensitivity: 100-130 |
| Office Work | Smoothing: 7-9, Sensitivity: 150-180 |
| Design/Drawing | Smoothing: 8-12, Sensitivity: 180-250 |
| Presentation | Smoothing: 6-8, Sensitivity: 120-150 |

### Troubleshooting

**Problem**: Cursor is too jittery
- **Solution**: Increase Smoothing Factor to 10-15

**Problem**: Cursor is too slow to respond
- **Solution**: Decrease Smoothing Factor to 3-5

**Problem**: Can't reach screen edges easily
- **Solution**: Decrease Mouse Sensitivity to 80-120

**Problem**: Cursor moves too much for small hand movements
- **Solution**: Increase Mouse Sensitivity to 200-250

**Problem**: Settings window closed accidentally
- **Solution**: Restart the application (press 'q' to quit, then run `python main.py` again)

## Technical Details

### How It Works

The Settings GUI runs in a **separate thread** alongside the OpenCV camera loop:
- Main thread: Handles camera capture and hand tracking
- GUI thread: Manages the tkinter settings window
- **Thread-safe**: Settings are read from the GUI thread and applied to the main thread in real-time

### Implementation

The settings are applied in two places:

1. **Smoothing Factor**: Updates `MouseController.smoothing_factor` every frame
2. **Mouse Sensitivity**: Updates padding values (padding_left, padding_right, padding_top, padding_bottom) used in coordinate interpolation

### Files Modified

- `settings_gui.py`: New file containing the SettingsGUI class
- `main.py`: Integrated with Settings GUI for real-time updates
- `mouse_controller.py`: No changes needed (smoothing_factor is public attribute)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit application (closes all windows) |
| `k` | Toggle virtual keyboard |
| `v` | Toggle voice control |

## Integration with Other Features

The Settings GUI works seamlessly with:
- ✓ Hand gesture controls
- ✓ Virtual keyboard
- ✓ Voice control
- ✓ Scroll mode
- ✓ Click gestures

All features continue to work while adjusting settings!

## Future Enhancements

Possible additions:
- Save/load settings profiles
- Keyboard shortcut to show/hide settings window
- More advanced parameters (buffer size, click threshold, etc.)
- Preset buttons for common scenarios

---

**Enjoy your enhanced Virtual Mouse experience!** 🖱️✨
