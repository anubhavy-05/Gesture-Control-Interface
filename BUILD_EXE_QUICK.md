# 🚀 PyInstaller Quick Commands

## Copy & Paste These Commands!

---

## ✨ THE COMMAND YOU NEED (Recommended)

```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

**This creates:**
- Single `VirtualMouse.exe` file
- No console window (only camera window)
- Located in `dist/` folder

---

## 📋 Step-by-Step

### 1. Install PyInstaller
```powershell
pip install pyinstaller
```

### 2. Navigate to Your Project
```powershell
cd "c:\Users\ay840\OneDrive\Desktop\APROJECT\Gesture-Control-Interface"
```

### 3. Build the EXE
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

### 4. Find Your EXE
```powershell
cd dist
```

Your EXE is here: `VirtualMouse.exe` 🎉

### 5. Test It
```powershell
.\VirtualMouse.exe
```

---

## 🔧 Alternative Commands

### If You Get Errors, Use This:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" --hidden-import mediapipe --hidden-import cv2 main.py
```

### With Custom Icon:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" --icon=icon.ico main.py
```

### Debug Mode (Shows Console):
```powershell
pyinstaller --onefile --console --name "VirtualMouse" main.py
```

### Clean Rebuild:
```powershell
Remove-Item -Recurse -Force build, dist
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

---

## 🎯 Console Window Control

### Hide Console (Only Camera Window):
```powershell
--noconsole
```
or
```powershell
--windowed
```

### Show Console (For Debugging):
```powershell
--console
```

---

## 📝 What Each Flag Means

| Flag | What It Does |
|------|--------------|
| `--onefile` | Creates single .exe (not a folder) |
| `--noconsole` | Hides black console window ✨ |
| `--windowed` | Same as --noconsole |
| `--console` | Shows console window (for debugging) |
| `--name "VirtualMouse"` | Names your exe file |
| `--icon=icon.ico` | Adds custom icon |
| `--hidden-import MODULE` | Forces inclusion of module |

---

## ⚡ Super Quick Reference

**Just want to build? Run this:**
```powershell
pip install pyinstaller && pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

**EXE location:**
```
dist/VirtualMouse.exe
```

**Run it:**
Double-click `VirtualMouse.exe` or:
```powershell
cd dist
.\VirtualMouse.exe
```

---

## 🎉 Done!

Your standalone app is ready to share with anyone on Windows - no Python needed!

**See [PYINSTALLER_GUIDE.md](PYINSTALLER_GUIDE.md) for detailed instructions and troubleshooting.**
