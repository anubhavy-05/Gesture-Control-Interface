# 🔍 TROUBLESHOOTING GUIDE

## ❌ "Code is not working" - HOW TO DEBUG

When you say "not working", please run these diagnostic tools to find the EXACT problem:

---

## 🚀 QUICK START - Run These Scripts:

### **Option 1: PowerShell (RECOMMENDED)**
```powershell
cd "c:\Users\ay840\OneDrive\Desktop\gesture\Gesture-Control-Interface\VIRTUAL-WORLD\RealTime-Frame-Puzzle"
.\RUN_WITH_ERRORS.ps1
```

### **Option 2: Command Prompt**
```cmd
cd "c:\Users\ay840\OneDrive\Desktop\gesture\Gesture-Control-Interface\VIRTUAL-WORLD\RealTime-Frame-Puzzle"
RUN_WITH_ERRORS.bat
```

### **Option 3: Manual Test**
```powershell
# 1. Activate virtual environment
& "C:/Users/ay840/OneDrive/Desktop/gesture/.venv/Scripts/Activate.ps1"

# 2. Run error finder
cd Gesture-Control-Interface\VIRTUAL-WORLD\RealTime-Frame-Puzzle
python find_error.py

# 3. If all checks pass, run main
python main.py
```

---

## 📊 What These Scripts Do:

### **find_error.py** - Finds exact problem
✅ Tests if OpenCV is installed  
✅ Tests if numpy is installed  
✅ Tests if webcam works (default backend)  
✅ Tests if webcam works (CAP_DSHOW backend)  
✅ Tests if hand_tracker.py can be imported  
✅ Tests if main.py has syntax errors  

### **RUN_WITH_ERRORS.bat / .ps1** - Shows full error
✅ Runs diagnostic first  
✅ Then runs main.py  
✅ Captures and displays ALL error messages  
✅ Shows exit code  

---

## 🎯 Common Problems & Solutions:

### Problem 1: ImportError - No module named 'cv2'
```
[ERROR] ModuleNotFoundError: No module named 'cv2'
```
**Fix:**
```powershell
& .venv\Scripts\Activate.ps1
pip install opencv-python numpy
```

---

### Problem 2: Webcam not opening
```
[ERROR] Could not access webcam!
```
**Fix:**
- Close other apps (Zoom, Teams, Skype, OBS)
- Check Windows Settings > Privacy > Camera (Allow apps)
- Try test_webcam.py first:
  ```powershell
  python test_webcam.py
  ```

---

### Problem 3: Hand tracker import fails
```
[ERROR] ModuleNotFoundError: No module named 'hand_tracker'
```
**Fix:**
- Check if `hand_tracker.py` exists in:
  `c:\Users\ay840\OneDrive\Desktop\gesture\Gesture-Control-Interface\hand_tracker.py`
- If missing, you need to create it or restore it

---

### Problem 4: Syntax Error
```
SyntaxError: invalid syntax
```
**Fix:**
- Run: `python find_error.py`
- It will show EXACT line number
- Check Python version: `python --version` (need 3.7+)

---

### Problem 5: Program starts but crashes immediately
**Symptoms:**
- Terminal closes instantly
- No error message visible

**Fix:**
- Run with `RUN_WITH_ERRORS.bat` or `RUN_WITH_ERRORS.ps1`
- These keep window open and show full error
- Copy the complete error message

---

## 📝 How to Report Problems:

When asking for help, provide:

1. **What script you ran:**
   ```
   Example: "I ran python main.py"
   ```

2. **Full error message:**
   ```
   Copy everything from terminal, including:
   - [ERROR] lines
   - Traceback
   - Line numbers
   ```

3. **Diagnostic results:**
   ```
   Run: python find_error.py
   Copy output showing which checks passed/failed
   ```

4. **Your environment:**
   ```
   - Python version: python --version
   - OpenCV version: pip show opencv-python
   - Virtual environment active? Yes/No
   ```

---

## 🔧 Quick Fixes Checklist:

Before asking "not working", check:

- [ ] Virtual environment activated?
  ```powershell
  & .venv\Scripts\Activate.ps1
  ```

- [ ] OpenCV installed?
  ```powershell
  pip list | Select-String opencv
  ```

- [ ] In correct directory?
  ```powershell
  cd Gesture-Control-Interface\VIRTUAL-WORLD\RealTime-Frame-Puzzle
  ```

- [ ] Webcam not used by other app?
  ```
  Close: Zoom, Teams, Skype, OBS, etc.
  ```

- [ ] Windows Camera permission enabled?
  ```
  Settings > Privacy > Camera > ON
  ```

---

## 🎯 Testing Workflow:

```
1. Run: python find_error.py
   ├─ All pass? → Continue to step 2
   └─ Fails? → Fix the specific error shown

2. Run: python test_webcam.py
   ├─ Webcam works? → Continue to step 3
   └─ Fails? → Fix webcam (close other apps, check privacy)

3. Run: python main.py
   ├─ Works? → Play the game! 🎉
   └─ Fails? → Run RUN_WITH_ERRORS.ps1 and send error message
```

---

## 📞 Getting Help:

If still not working after running diagnostics:

1. Run: `.\RUN_WITH_ERRORS.ps1`
2. Copy the COMPLETE output
3. Share:
   - Full error message
   - Which diagnostic checks failed
   - Python version
   - What you were trying to do

**Without this info, I can't help debug "not working"!**

---

## ✅ Success Indicators:

You know it's working when:

1. **find_error.py shows:**
   ```
   ✓ cv2 imported
   ✓ numpy imported
   ✓ Webcam working
   ✓ No syntax errors
   ALL CHECKS PASSED!
   ```

2. **main.py shows:**
   ```
   [SUCCESS] Webcam opened successfully
   [INFO] Press SPACE to capture, ESC to exit
   ```

3. **Window appears:**
   - Live camera feed visible
   - Can press SPACE to capture
   - No crashes

---

## 🚀 Let's Debug Together!

Run one of these and share the output:

```powershell
# Method 1 (Best)
.\RUN_WITH_ERRORS.ps1

# Method 2 (Alternative)
python find_error.py

# Method 3 (Direct test)
python test_webcam.py
```

**Copy the complete output and share it!** 📋

---

*Created: March 12, 2026*  
*Purpose: Help debug "not working" issues properly*
