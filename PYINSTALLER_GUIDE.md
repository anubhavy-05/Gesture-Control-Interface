# 📦 PyInstaller Guide - Create Standalone EXE

## Complete guide to convert your Virtual Mouse Python project into a single .exe file

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Working Python script (main.py)
- ✅ All dependencies installed
- ✅ Python 3.7+ installed
- ✅ Windows OS (for .exe creation)

---

## 🔧 Step 1: Install PyInstaller

Open PowerShell or Command Prompt and run:

```powershell
pip install pyinstaller
```

Verify installation:
```powershell
pyinstaller --version
```

---

## 🚀 Step 2: Create the EXE (Basic)

### Option A: Simple One-File EXE (Recommended)

Navigate to your project folder:
```powershell
cd "c:\Users\ay840\OneDrive\Desktop\APROJECT\Gesture-Control-Interface"
```

Create a single-file EXE **WITHOUT console window**:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

**Explanation:**
- `--onefile` - Creates a single .exe file (not a folder)
- `--noconsole` - Hides the black console window ✨
- `--name "VirtualMouse"` - Names your app "VirtualMouse.exe"
- `main.py` - Your main Python script

### Option B: With Icon (Optional)

If you want a custom icon:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" --icon=icon.ico main.py
```

*(You'll need to create or download an icon.ico file first)*

---

## 🎯 Step 3: Full Command with All Options

For your OpenCV + MediaPipe project, use this comprehensive command:

```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" --add-data "README.md;." main.py
```

**Advanced Options:**
- `--add-data "README.md;."` - Include additional files (use `;` on Windows, `:` on Linux/Mac)
- `--hidden-import mediapipe` - Explicitly include MediaPipe if PyInstaller misses it
- `--hidden-import cv2` - Explicitly include OpenCV if needed

### Full Command (If issues occur):
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" ^
    --hidden-import mediapipe ^
    --hidden-import cv2 ^
    --hidden-import numpy ^
    --hidden-import pyautogui ^
    --hidden-import PIL ^
    main.py
```

*(The `^` allows multi-line commands in PowerShell)*

---

## 📁 Step 4: Find Your EXE

After PyInstaller finishes (takes 1-5 minutes), you'll find:

```
Gesture-Control-Interface/
├── build/              ← Temporary build files
├── dist/               ← YOUR EXE IS HERE! 🎉
│   └── VirtualMouse.exe
├── VirtualMouse.spec   ← PyInstaller configuration
├── main.py
└── ... (other files)
```

**Your standalone EXE:** `dist/VirtualMouse.exe`

---

## 🎬 Step 5: Test Your EXE

1. Navigate to the `dist` folder:
   ```powershell
   cd dist
   ```

2. Double-click `VirtualMouse.exe` or run:
   ```powershell
   .\VirtualMouse.exe
   ```

3. **Expected behavior:**
   - ✅ Only the camera window opens
   - ✅ No black console window
   - ✅ All features work normally

---

## 🐛 Troubleshooting

### Issue 1: "Failed to execute script main"

**Solution:** Add hidden imports:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" ^
    --hidden-import mediapipe ^
    --hidden-import mediapipe.python ^
    --hidden-import cv2 ^
    main.py
```

### Issue 2: "Module not found: mediapipe"

**Solution:** Use `--collect-all` for MediaPipe:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" ^
    --collect-all mediapipe ^
    main.py
```

### Issue 3: EXE is too large (>200MB)

**Normal!** OpenCV and MediaPipe are large libraries. Your EXE will be ~150-300MB.

**To reduce size:**
- Use `--onedir` instead of `--onefile` (creates a folder with dependencies)
- Remove unused imports from your code

### Issue 4: Webcam doesn't open

**Solution:** Check camera permissions in Windows Settings:
- Go to Settings > Privacy > Camera
- Allow desktop apps to access camera

### Issue 5: Console window still shows

**Make sure you used `--noconsole`** (not `--console`).

If it still shows, use `--windowed`:
```powershell
pyinstaller --onefile --windowed --name "VirtualMouse" main.py
```

(`--windowed` is an alias for `--noconsole`)

### Issue 6: "VCRUNTIME140.dll missing"

**Solution:** Install Visual C++ Redistributable:
- Download from Microsoft's website
- Or include the DLL in your build

### Issue 7: Settings GUI doesn't appear

**Solution:** Add tkinter explicitly:
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" ^
    --hidden-import tkinter ^
    main.py
```

---

## 🎨 Advanced: Using a Spec File

For more control, edit the `.spec` file PyInstaller creates:

1. Generate the spec file first:
   ```powershell
   pyi-makespec --onefile --noconsole --name "VirtualMouse" main.py
   ```

2. Edit `VirtualMouse.spec`:
   ```python
   # -*- mode: python ; coding: utf-8 -*-
   
   block_cipher = None
   
   a = Analysis(
       ['main.py'],
       pathex=[],
       binaries=[],
       datas=[('README.md', '.')],  # Add your files here
       hiddenimports=['mediapipe', 'cv2', 'numpy', 'pyautogui'],
       hookspath=[],
       hooksconfig={},
       runtime_hooks=[],
       excludes=[],
       win_no_prefer_redirects=False,
       win_private_assemblies=False,
       cipher=block_cipher,
       noarchive=False,
   )
   pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
   
   exe = EXE(
       pyz,
       a.scripts,
       a.binaries,
       a.zipfiles,
       a.datas,
       [],
       name='VirtualMouse',
       debug=False,
       bootloader_ignore_signals=False,
       strip=False,
       upx=True,
       upx_exclude=[],
       runtime_tmpdir=None,
       console=False,  # ← This hides the console!
       disable_windowed_traceback=False,
       argv_emulation=False,
       target_arch=None,
       codesign_identity=None,
       entitlements_file=None,
       icon='icon.ico'  # Add your icon here
   )
   ```

3. Build from spec file:
   ```powershell
   pyinstaller VirtualMouse.spec
   ```

---

## 📊 Build Process Timeline

```
1. PyInstaller analyzes dependencies    [▓▓▓░░░░░░░] 30s
2. Collecting modules                   [▓▓▓▓▓▓░░░░] 60s
3. Bundling files                       [▓▓▓▓▓▓▓▓░░] 90s
4. Creating executable                  [▓▓▓▓▓▓▓▓▓▓] 120s
5. Done! ✅
```

Total time: **2-5 minutes** (depending on your PC)

---

## 🎯 Console Window Options

### Option 1: No Console (Recommended for GUI apps)
```powershell
--noconsole
# or
--windowed
```

**Result:** Only camera window opens, no black CMD window

### Option 2: With Console (For debugging)
```powershell
--console
```

**Result:** Black CMD window + camera window (useful for seeing errors)

### Option 3: Hide Console but Keep Error Messages

Edit your `main.py` to create a log file:
```python
import sys
import os

# Redirect errors to log file when frozen
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    log_file = open('error_log.txt', 'w')
    sys.stderr = log_file
    sys.stdout = log_file
```

Then use `--noconsole` and check `error_log.txt` if issues occur.

---

## 📦 Distribution

Once you have `VirtualMouse.exe`:

### Single EXE Distribution
- ✅ Share just the `VirtualMouse.exe` file
- ✅ Users don't need Python installed
- ✅ No installation required - just double-click to run!

### Folder Distribution (if using --onedir)
- Share the entire `dist/VirtualMouse/` folder
- Users run `VirtualMouse.exe` inside the folder
- Smaller individual files, but more files total

### Creating an Installer (Optional)
Use **Inno Setup** or **NSIS** to create a proper installer:
- Adds Start Menu shortcuts
- Creates Desktop icon
- Handles uninstallation
- Professional appearance

---

## ⚡ Quick Reference Commands

### Fastest: Simple EXE without console
```powershell
pyinstaller --onefile --noconsole main.py
```

### Recommended: Named EXE without console
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

### With Icon: Custom icon without console
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" --icon=icon.ico main.py
```

### Debug Mode: With console (for testing)
```powershell
pyinstaller --onefile --console --name "VirtualMouse" main.py
```

### Full Featured: Everything included
```powershell
pyinstaller --onefile --noconsole --name "VirtualMouse" ^
    --icon=icon.ico ^
    --hidden-import mediapipe ^
    --hidden-import cv2 ^
    main.py
```

---

## 🎓 Tips & Best Practices

### 1. **Clean Build**
If you need to rebuild, delete the `build/` and `dist/` folders first:
```powershell
Remove-Item -Recurse -Force build, dist
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

### 2. **Test on Another PC**
Your EXE should work on other Windows PCs **without Python installed**. Test it!

### 3. **Antivirus False Positives**
Some antivirus software flags PyInstaller EXEs as suspicious. This is normal. You may need to:
- Add an exception in antivirus
- Sign your EXE with a code signing certificate (advanced)

### 4. **File Size**
Expect 150-300MB due to MediaPipe and OpenCV. This is normal and unavoidable.

### 5. **Debugging**
Build with `--console` first to see error messages, then rebuild with `--noconsole` once working.

### 6. **Virtual Environment**
Build from a clean virtual environment to minimize EXE size:
```powershell
python -m venv build_env
.\build_env\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
```

---

## 🚀 Final Steps

1. **Build the EXE:**
   ```powershell
   pyinstaller --onefile --noconsole --name "VirtualMouse" main.py
   ```

2. **Test it:**
   ```powershell
   cd dist
   .\VirtualMouse.exe
   ```

3. **Verify:**
   - ✅ Only camera window opens (no console)
   - ✅ Hand tracking works
   - ✅ Settings GUI appears
   - ✅ All gestures work

4. **Distribute:**
   - Share `VirtualMouse.exe` with anyone
   - No Python required on their PC!
   - Just double-click to run

---

## 📚 Additional Resources

- **PyInstaller Docs:** https://pyinstaller.org/
- **Troubleshooting:** https://pyinstaller.org/en/stable/when-things-go-wrong.html
- **Hidden Imports:** https://pyinstaller.org/en/stable/hooks.html

---

## 🎉 Success!

You now have a **professional standalone application** that:
- ✅ Runs without Python
- ✅ Shows only the camera window (no console)
- ✅ Can be shared with anyone on Windows
- ✅ Works just like the Python version

**Enjoy your portable Virtual Mouse application!** 🖱️✨

---

## ⚠️ Important Notes

1. **First Run**: First time running the EXE takes longer (5-10 seconds) as it extracts to temp folder
2. **Firewall**: Windows may ask for firewall permission - click "Allow"
3. **Camera Permission**: Ensure camera access is enabled in Windows Settings
4. **File Size**: Don't worry about 200MB+ size - normal for OpenCV apps
5. **Updates**: To update, rebuild the EXE with the new code

---

**Need help?** Check the troubleshooting section or run with `--console` to see error messages!
