# Settings GUI - Quick Reference Card

## 🎛️ What It Does
Adjust your Virtual Mouse settings in **real-time** without restarting!

## 🚀 Quick Start
```bash
python main.py
```
Two windows will open:
1. **Camera View** (OpenCV) - Hand tracking
2. **Settings Panel** (Tkinter) - Control sliders

## 🎚️ Sliders

### Smoothing Factor (1-20)
```
1-5    🏃 FAST        - Quick response, more jitter
6-10   ⚖️ BALANCED   - Recommended for most users
11-20  🐌 SMOOTH     - Very smooth, slower response
```

### Mouse Sensitivity (50-300px)
```
50-100   🎯 EASY      - Easy to reach screen edges
100-200  ⚖️ BALANCED  - Recommended for most users
200-300  🎨 PRECISE   - Precise control, more hand movement
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| Drag Sliders | Adjust settings |
| Reset Button | Restore defaults (7, 150) |
| X (close) | Close GUI (will reopen on restart) |
| `q` (camera window) | Quit entire application |

## 💡 Tips

### Finding Your Sweet Spot
1. Start with **defaults** (7, 150)
2. Test cursor movement
3. Too jittery? ➜ Increase **Smoothing**
4. Too slow? ➜ Decrease **Smoothing**
5. Can't reach edges? ➜ Decrease **Sensitivity**
6. Too sensitive? ➜ Increase **Sensitivity**

### Common Use Cases

**For Gaming** 🎮
- Smoothing: 4-6
- Sensitivity: 100-130

**For Office Work** 💼
- Smoothing: 7-9
- Sensitivity: 150-180

**For Design/Art** 🎨
- Smoothing: 8-12
- Sensitivity: 180-250

**For Presentations** 📊
- Smoothing: 6-8
- Sensitivity: 120-150

## 📊 Where Values Appear

1. **Settings Window** - Current value label under each slider
2. **Camera Window** - Top left corner shows: `Smoothing: 7 | Sensitivity: 150px`

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Cursor too jittery | Increase Smoothing to 10-15 |
| Cursor too slow | Decrease Smoothing to 3-5 |
| Can't reach screen edges | Decrease Sensitivity to 80-120 |
| Cursor too sensitive | Increase Sensitivity to 200-250 |
| Settings window closed | Restart app (`q` then `python main.py`) |
| Changes don't apply | Make sure cursor is moving (index finger up) |

## 🔧 Technical Info

- **Thread-Safe**: GUI runs in separate thread
- **Zero Lag**: No performance impact on hand tracking
- **Instant Apply**: Changes take effect immediately
- **No Restart**: Adjust while application is running

## 📚 Full Documentation

For detailed guide, see: **[SETTINGS_GUI_GUIDE.md](SETTINGS_GUI_GUIDE.md)**

---

**Remember**: You can always click **Reset to Defaults** if you get lost! 🔄
