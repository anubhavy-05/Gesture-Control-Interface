"""
Webcam Test Script - Diagnose webcam issues
"""

import cv2
import sys

print("=" * 60)
print("WEBCAM DIAGNOSTIC TEST")
print("=" * 60)

print("\n[1] Testing Default Backend...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✓ Default backend: WORKING")
    ret, frame = cap.read()
    if ret:
        print(f"✓ Frame size: {frame.shape[1]}x{frame.shape[0]}")
    else:
        print("✗ Cannot read frames")
    cap.release()
else:
    print("✗ Default backend: FAILED")

print("\n[2] Testing CAP_DSHOW Backend...")
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if cap.isOpened():
        print("✓ CAP_DSHOW backend: WORKING")
        ret, frame = cap.read()
        if ret:
            print(f"✓ Frame size: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("✗ Cannot read frames")
        cap.release()
    else:
        print("✗ CAP_DSHOW backend: FAILED")
except Exception as e:
    print(f"✗ CAP_DSHOW backend: ERROR - {e}")

print("\n[3] Testing Live Preview...")
print("Opening webcam window...")
print("Press 'q' to close window and finish test")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("✗ Cannot open webcam for live preview")
    sys.exit(1)

# Show live preview for 5 seconds or until 'q' is pressed
frame_count = 0
while frame_count < 150:  # 5 seconds at 30fps
    ret, frame = cap.read()
    if not ret:
        print("✗ Failed to read frame")
        break
    
    # Add text overlay
    cv2.putText(frame, "Webcam Test - Press 'q' to quit", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Frame: {frame_count}", 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    cv2.imshow("Webcam Test - Working!", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("✓ User quit test")
        break
    
    frame_count += 1

cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 60)
if frame_count > 0:
    print("✓ SUCCESS: Webcam is working properly!")
    print(f"  Captured {frame_count} frames")
    print("\nYou can now run main.py")
else:
    print("✗ FAILED: Webcam test failed")
    print("\nTroubleshooting:")
    print("  1. Check if webcam is connected")
    print("  2. Close other apps (Zoom, Skype, Teams)")
    print("  3. Check Windows Privacy > Camera settings")
    print("  4. Try a different USB port")
    print("  5. Restart computer")
print("=" * 60)
