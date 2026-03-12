"""
MINIMAL TEST - Find exact error
Run this to see what's failing
"""
import sys
import os

# Add paths exactly like main.py does
script_dir = os.path.dirname(os.path.abspath(__file__))
virtual_world_dir = os.path.dirname(script_dir)
parent_dir = os.path.dirname(virtual_world_dir)
sys.path.insert(0, parent_dir)

print("=" * 60)
print("MINIMAL ERROR FINDER")
print("=" * 60)
print()

# Step 1: Test imports
print("[1/6] Testing imports...")
try:
    import cv2
    print("    ✓ cv2 (OpenCV) imported")
except ImportError as e:
    print(f"    ✗ FAILED: {e}")
    print("\n    FIX: pip install opencv-python")
    sys.exit(1)

try:
    import numpy as np
    print("    ✓ numpy imported")
except ImportError as e:
    print(f"    ✗ FAILED: {e}")
    print("\n    FIX: pip install numpy")
    sys.exit(1)

try:
    import time
    print("    ✓ time imported")
except ImportError as e:
    print(f"    ✗ FAILED: {e}")
    sys.exit(1)

try:
    import random
    print("    ✓ random imported")
except ImportError as e:
    print(f"    ✗ FAILED: {e}")
    sys.exit(1)

# Step 2: Test hand_tracker import
print("\n[2/6] Testing hand_tracker import...")
try:
    from hand_tracker import HandDetector
    print("    ✓ HandDetector imported")
except ImportError as e:
    print(f"    ✗ FAILED: {e}")
    print(f"\n    hand_tracker.py location: {parent_dir}\\hand_tracker.py")
    print(f"    Exists: {os.path.exists(os.path.join(parent_dir, 'hand_tracker.py'))}")

# Step 3: Test webcam with default backend
print("\n[3/6] Testing webcam (default backend)...")
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"    ✓ Webcam working: {frame.shape}")
        else:
            print("    ✗ Webcam opened but can't read frames")
        cap.release()
    else:
        print("    ✗ Cannot open webcam")
except Exception as e:
    print(f"    ✗ ERROR: {e}")

# Step 4: Test webcam with CAP_DSHOW
print("\n[4/6] Testing webcam (CAP_DSHOW backend)...")
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    time.sleep(0.5)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"    ✓ CAP_DSHOW working: {frame.shape}")
        else:
            print("    ✗ CAP_DSHOW opened but can't read frames")
        cap.release()
    else:
        print("    ✗ Cannot open webcam with CAP_DSHOW")
except Exception as e:
    print(f"    ✗ ERROR: {e}")

# Step 5: Test main.py syntax
print("\n[5/6] Testing main.py syntax...")
try:
    import py_compile
    py_compile.compile('main.py', doraise=True)
    print("    ✓ No syntax errors in main.py")
except Exception as e:
    print(f"    ✗ SYNTAX ERROR: {e}")
    sys.exit(1)

# Step 6: Test actual import of main
print("\n[6/6] Testing if main.py can be imported...")
try:
    # This will catch any runtime errors when loading main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
        compile(code, 'main.py', 'exec')
    print("    ✓ main.py compiles successfully")
except SyntaxError as e:
    print(f"    ✗ SYNTAX ERROR at line {e.lineno}:")
    print(f"       {e.text}")
    print(f"       {e.msg}")
    sys.exit(1)
except Exception as e:
    print(f"    ✗ ERROR: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL CHECKS PASSED!")
print("=" * 60)
print("\nIf this passes but main.py still fails, run:")
print("    python main.py 2>&1 | more")
print("\nAnd copy the FULL error message!")
print("=" * 60)
