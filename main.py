"""
AI Virtual Mouse - Main Entry Point
Control your mouse cursor using hand gestures captured through your webcam.

Gestures:
- Index finger up: Move mouse cursor
- Index finger + Thumb close (<30px): Left click
- Middle finger + Thumb close (<30px): Right click
- Ring finger folded (with index up): Double click
- Pinky finger up (only): Scroll mode - move hand up/down to scroll
- All fingers up (Open Palm): Alternative scroll mode
"""

import cv2
import time
import math
import numpy as np
from hand_tracker import HandDetector
from mouse_controller import MouseController
from virtual_keyboard import VirtualKeyboard
from voice_control import VoiceController
from settings_gui import SettingsGUI


def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    
    Args:
        point1 (tuple): (id, x, y) of the first point.
        point2 (tuple): (id, x, y) of the second point.
    
    Returns:
        float: The distance between the two points.
    """
    x1, y1 = point1[1], point1[2]
    x2, y2 = point2[1], point2[2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def main():
    """
    Main function to run the AI Virtual Mouse application.
    """
    print("="*50)
    print("AI Virtual Mouse - Starting...")
    print("="*50)
    
    # Initialize hand detector and mouse controller first
    try:
        print("\n[1/3] Initializing hand detector...")
        detector = HandDetector(max_hands=1, detection_confidence=0.7, tracking_confidence=0.7)
        print("✓ Hand detector initialized")
    except Exception as e:
        print(f"✗ Error initializing hand detector: {e}")
        return
    
    try:
        print("\n[2/3] Initializing mouse controller...")
        mouse = MouseController(smoothing_factor=7)
        print(f"✓ Mouse controller initialized (Screen: {mouse.screen_width}x{mouse.screen_height})")
    except Exception as e:
        print(f"✗ Error initializing mouse controller: {e}")
        return
    
    # Initialize settings GUI
    try:
        print("\n[2.25/3] Initializing settings GUI...")
        settings_gui = SettingsGUI()
        settings_gui.start()
        print("✓ Settings GUI initialized")
        print("  Note: Settings window will appear alongside the camera view")
    except Exception as e:
        print(f"✗ Warning: Could not initialize settings GUI: {e}")
        print("  Settings GUI will not be available")
        settings_gui = None
    
    # Initialize virtual keyboard
    try:
        print("\n[2.5/3] Initializing virtual keyboard...")
        keyboard = VirtualKeyboard(frame_width=640, frame_height=480)
        keyboard_visible = False  # Start with keyboard hidden
        print("✓ Virtual keyboard initialized")
    except Exception as e:
        print(f"✗ Error initializing virtual keyboard: {e}")
        return
    
    # Voice status variables
    voice_last_command = ""
    voice_command_time = 0
    
    # Voice callback function to handle voice commands and status
    def voice_callback(message):
        nonlocal voice_last_command, voice_command_time, keyboard_visible
        voice_last_command = message
        voice_command_time = time.time()
        
        # Handle special keyboard commands
        if message == "SHOW_KEYBOARD":
            keyboard_visible = True
        elif message == "HIDE_KEYBOARD":
            keyboard_visible = False
    
    # Initialize voice controller
    try:
        print("\n[2.75/3] Initializing voice controller...")
        voice = VoiceController(callback=voice_callback)
        voice_active = False  # Start with voice control off
        print("✓ Voice controller initialized")
        print("  Note: Voice control is OFF by default")
        print("  Press 'v' to start/stop voice control")
    except Exception as e:
        print(f"✗ Warning: Could not initialize voice controller: {e}")
        print("  Voice control will not be available")
        print("  Install: pip install SpeechRecognition pyaudio")
        voice = None
        voice_active = False
    
    # Initialize webcam
    print("\n[3/3] Opening webcam...")
    capture = cv2.VideoCapture(0)
    
    # Try alternative camera indices if 0 fails
    if not capture.isOpened():
        print("⚠ Camera 0 not available, trying camera 1...")
        capture = cv2.VideoCapture(1)
    
    if not capture.isOpened():
        print("✗ Error: Could not open webcam.")
        print("Please check:")
        print("  - Is your webcam connected?")
        print("  - Is another application using the webcam?")
        print("  - Do you have webcam permissions enabled?")
        return
    
    # Set webcam properties
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Verify we can read a frame
    ret, test_frame = capture.read()
    if not ret or test_frame is None:
        print("✗ Error: Webcam opened but cannot read frames.")
        capture.release()
        return
    
    print(f"✓ Webcam opened successfully ({test_frame.shape[1]}x{test_frame.shape[0]})")
    print("\n" + "="*50)
    print("READY! Webcam window will open now...")
    print("="*50)
    
    # Variables for FPS calculation
    prev_time = 0
    
    # Variables for click detection
    left_click_performed = False
    right_click_performed = False
    double_click_performed = False
    click_cooldown_time = 0.5  # Cooldown period in seconds to prevent multiple clicks
    last_left_click_time = 0
    last_right_click_time = 0
    last_double_click_time = 0
    
    # Variables for scroll detection
    scroll_mode_active = False
    prev_hand_y = None  # Track previous hand position for scroll detection
    scroll_threshold = 15  # Minimum vertical movement to trigger scroll
    scroll_sensitivity = 1  # Scroll speed multiplier
    
    # Distance threshold for finger-thumb proximity
    click_distance_threshold = 30
    
    # Frame dimensions (will be updated when first frame is captured)
    frame_width = 640
    frame_height = 480
    
    print("  - Pinky finger up (only): Scroll Mode")
    print("  - All fingers up (Open Palm): Alternative Scroll Mode")
    print("AI Virtual Mouse Started!")
    print("Gestures:")
    print("  - Index finger up: Move mouse")
    print("  - Index + Thumb close (<30px): Left Click")
    print("  - Middle + Thumb close (<30px): Right Click")
    print("  - Ring finger folded: Double Click")
    print("\nKeyboard Controls:")
    print("  - Press 'k' to toggle virtual keyboard")
    print("  - Hover over a key for 1 second to type")
    print("  - Or click on a key to type immediately")
    print("\nVoice Controls:")
    print("  - Press 'v' to toggle voice control")
    print("  - Say 'Open Chrome', 'Type Hello', 'Enter', etc.")
    print("  - Say 'Show Keyboard' or 'Hide Keyboard'")
    print("\nSettings GUI:")
    print("  - A separate window is now open with sliders")
    print("  - Adjust Smoothing Factor to control cursor jitter")
    print("  - Adjust Mouse Sensitivity to change screen edge reachability")
    print("  - Changes apply in real-time!")
    print("\nPress 'q' to quit.")
    
    while True:
        # Capture frame from webcam
        success, frame = capture.read()
        
        # Handle case where frame capture fails
        if not success or frame is None:
            print("Warning: Failed to capture frame from webcam.")
            continue
        
        # Update frame dimensions
        frame_height, frame_width, _ = frame.shape
        
        # Flip frame horizontally for mirror effect (more intuitive)
        frame = cv2.flip(frame, 1)
        
        # Detect hands and draw landmarks
        frame = detector.findHands(frame, draw=True)
        
        # Find hand landmarks
        landmark_list = detector.findPosition(frame, hand_number=0)
        
        # Check if hand is detected
        if len(landmark_list) > 0:
            # Get finger status (which fingers are up)
            fingers = detector.fingersUp(landmark_list)
            
            # Debug: Display finger states
            finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            debug_text = ' | '.join([f"{name}: {fingers[i]}" for i, name in enumerate(finger_names)])
            cv2.putText(frame, debug_text, (10, frame_height - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Extract key landmark positions
            # Landmark 4: Thumb tip
            # Landmark 8: Index finger tip
            # Landmark 12: Middle finger tip
            # Landmark 20: Pinky finger tip
            # Landmark 0: Wrist (base of palm)
            thumb_tip = landmark_list[4]
            index_finger_tip = landmark_list[8]
            middle_finger_tip = landmark_list[12]
            ring_finger_tip = landmark_list[16]
            ring_finger_pip = landmark_list[14]  # PIP joint for ring finger
            pinky_tip = landmark_list[20]
            wrist = landmark_list[0]  # Wrist position for tracking hand movement
            ring_finger_tip = landmark_list[16]
            ring_finger_pip = landmark_list[14]  # PIP joint for ring finger
            
            # Calculate distances for gesture detection
            dist_index_thumb = calculate_distance(index_finger_tip, thumb_tip)
            dist_middle_thumb = calculate_distance(middle_finger_tip, thumb_tip)
            
            # Check if ring finger is folded (tip below PIP joint)
            ring_finger_folded = ring_finger_tip[2] > ring_finger_pip[2]
            
            current_time = time.time()
            
            # Get dynamic padding from settings GUI (if available)
            # Default to 150 if settings GUI is not available
            if settings_gui:
                padding_value = settings_gui.get_mouse_sensitivity()
            else:
                padding_value = 150
            
            # Define padding for coordinate mapping (used in both Mode 1 and Mode 2)
            # Larger padding = smaller camera area maps to full screen
            # Adjust these values: Higher = easier to reach screen edges
            padding_left = padding_value
            padding_right = padding_value
            padding_top = padding_value
            padding_bottom = padding_value
            
            # Mode 1: Only Index finger is up -> Move mouse
            if fingers[1] == 1 and fingers[2] == 0:  # Index up, Middle down
                # Get index finger tip position
                x, y = index_finger_tip[1], index_finger_tip[2]
                
                # Update mouse controller smoothing factor from settings GUI
                if settings_gui:
                    mouse.smoothing_factor = settings_gui.get_smoothing_factor()
                
                screen_x = np.interp(x, [padding_left, frame_width - padding_right], 
                    [0, mouse.screen_width])
                screen_y = np.interp(y, [padding_top, frame_height - padding_bottom], 
                    [0, mouse.screen_height])
                
                # Move the cursor
                mouse.moveCursor(screen_x, screen_y)
                
                # Draw a circle on the index finger tip for visual feedback
                cv2.circle(frame, (x, y), 15, (0, 255, 0), cv2.FILLED)
                
                # Display cursor mode indicator
                cv2.putText(frame, "MOVE MODE", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Check for LEFT CLICK gesture (Index + Thumb close)
                if dist_index_thumb < click_distance_threshold:
                    if not left_click_performed and (current_time - last_left_click_time > click_cooldown_time):
                        mouse.click(button='left')
                        print(f"✓ LEFT CLICK! Index-Thumb distance: {int(dist_index_thumb)}px")
                        left_click_performed = True
                        last_left_click_time = current_time
                        
                        # Visual feedback
                        cv2.putText(frame, "LEFT CLICK!", (10, 150), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        cv2.circle(frame, (x, y), 25, (0, 255, 255), 3)
                else:
                    left_click_performed = False
                
                # Display distance for debugging
                cv2.putText(frame, f"Index-Thumb: {int(dist_index_thumb)}px", (10, 180), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Mode 2: Middle finger is up -> Check for RIGHT CLICK
            elif fingers[2] == 1:  # Middle finger up
                # Get middle finger tip position for cursor tracking
                x, y = middle_finger_tip[1], middle_finger_tip[2]
                
                # Update mouse controller smoothing factor from settings GUI
                if settings_gui:
                    mouse.smoothing_factor = settings_gui.get_smoothing_factor()
                
                # Map webcam coordinates to screen coordinates
                screen_x = np.interp(x, [padding_left, frame_width - padding_right], 
                    [0, mouse.screen_width])
                screen_y = np.interp(y, [padding_top, frame_height - padding_bottom], 
                    [0, mouse.screen_height])
                
                # Move the cursor
                mouse.moveCursor(screen_x, screen_y)
                
                # Draw a circle on the middle finger tip
                cv2.circle(frame, (x, y), 15, (255, 165, 0), cv2.FILLED)
                
                # Display mode indicator
                cv2.putText(frame, "RIGHT CLICK MODE", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
                
                # Check for RIGHT CLICK gesture (Middle + Thumb close)
                if dist_middle_thumb < click_distance_threshold:
                    if not right_click_performed and (current_time - last_right_click_time > click_cooldown_time):
                        mouse.click(button='right')
                        print(f"✓ RIGHT CLICK! Middle-Thumb distance: {int(dist_middle_thumb)}px")
                        right_click_performed = True
                        last_right_click_time = current_time
                        
                        # Visual feedback
                        cv2.putText(frame, "RIGHT CLICK!", (10, 150), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
                        cv2.circle(frame, (x, y), 25, (0, 100, 255), 3)
                else:
                    right_click_performed = False
                
                # Display distance for debugging
                cv2.putText(frame, f"Middle-Thumb: {int(dist_middle_thumb)}px", (10, 180), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Mode 3: Check for DOUBLE CLICK gesture (Ring finger folded)
            if ring_finger_folded and fingers[1] == 1:  # Ring folded and index up
                if not double_click_performed and (current_time - last_double_click_time > click_cooldown_time):
                    mouse.doubleClick()
                    print(f"✓ DOUBLE CLICK! Ring finger folded")
                    double_click_performed = True
                    last_double_click_time = current_time
                    
                    # Visual feedback
                    cv2.putText(frame, "DOUBLE CLICK!", (frame_width // 2 - 100, frame_height // 2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)
            else:
                if not ring_finger_folded:
                    double_click_performed = False
            
            # Mode 4: SCROLL MODE - Pinky finger up (only) or All fingers up (Open Palm)
            # Check for Pinky Only mode (recommended - more precise)
            pinky_only_mode = fingers[4] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0
            
            # Check for Open Palm mode (all fingers up)
            open_palm_mode = all(fingers)
            
            if pinky_only_mode or open_palm_mode:
                scroll_mode_active = True
                
                # Get current hand position (using wrist as reference point)
                current_hand_y = wrist[2]
                
                # Visual feedback for scroll mode
                mode_text = "SCROLL MODE (Pinky)" if pinky_only_mode else "SCROLL MODE (Palm)"
                cv2.putText(frame, mode_text, (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                
                # Draw indicator circle on pinky or palm center
                indicator_x = pinky_tip[1] if pinky_only_mode else wrist[1]
                indicator_y = pinky_tip[2] if pinky_only_mode else wrist[2]
                cv2.circle(frame, (indicator_x, indicator_y), 15, (255, 0, 255), cv2.FILLED)
                
                # If we have a previous position, calculate movement and scroll
                if prev_hand_y is not None:
                    # Calculate vertical movement (delta_y)
                    delta_y = prev_hand_y - current_hand_y
                    
                    # Only scroll if movement exceeds threshold
                    if abs(delta_y) > scroll_threshold:
                        # Calculate scroll amount (positive = scroll up, negative = scroll down)
                        scroll_amount = int((delta_y / scroll_threshold) * scroll_sensitivity)
                        
                        # Perform scroll
                        mouse.scroll(scroll_amount)
                        
                        # Visual feedback with direction arrow
                        scroll_direction = "UP ↑" if delta_y > 0 else "DOWN ↓"
                        cv2.putText(frame, f"SCROLLING {scroll_direction}", (10, 150), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                        
                        print(f"✓ SCROLL {scroll_direction}: {scroll_amount} units (delta: {int(delta_y)}px)")
                
                # Update previous hand position
                prev_hand_y = current_hand_y
            else:
                # Reset scroll mode
                scroll_mode_active = False
                prev_hand_y = None
        
        else:
            # No hand detected - display message
            cv2.putText(frame, "No hand detected", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Virtual Keyboard Overlay and Interaction
        if keyboard_visible:
            # Draw keyboard on frame
            frame = keyboard.draw_keyboard(frame)
            
            # Check for keyboard interaction if hand is detected
            if len(landmark_list) > 0:
                # Get current cursor position in frame coordinates
                # Use index finger tip for keyboard interaction
                if fingers[1] == 1:  # Index finger is up
                    cursor_x = index_finger_tip[1]
                    cursor_y = index_finger_tip[2]
                    
                    # Check hover on keyboard
                    hovered_key, hover_progress = keyboard.check_hover(cursor_x, cursor_y)
                    
                    if hovered_key:
                        # Draw hover indicator
                        frame = keyboard.draw_hover_indicator(frame, hovered_key, hover_progress)
                    
                    # Check for click gesture on keyboard
                    if dist_index_thumb < click_distance_threshold:
                        if not left_click_performed:
                            # Perform keyboard click instead of mouse click
                            clicked_key = keyboard.handle_click(cursor_x, cursor_y)
            
            # Show last typed key
            frame = keyboard.get_typed_text_display(frame)
            
            # Display keyboard mode indicator
            cv2.putText(frame, "KEYBOARD MODE (Press 'k' to hide)", (10, frame_height - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        
        # Display voice control status
        if voice and voice_active:
            cv2.putText(frame, "VOICE: ON", (frame_width - 150, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display last voice command for 3 seconds
            if voice_last_command and (time.time() - voice_command_time < 3.0):
                cv2.putText(frame, f"Voice: {voice_last_command}", (10, frame_height - 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        elif voice:
            cv2.putText(frame, "VOICE: OFF", (frame_width - 150, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 2)
        
        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display control instructions on the frame
        cv2.putText(frame, "Press 'q' to quit", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Display current settings from GUI (if available)
        if settings_gui:
            settings_text = f"Smoothing: {settings_gui.get_smoothing_factor()} | Sensitivity: {settings_gui.get_mouse_sensitivity()}px"
            cv2.putText(frame, settings_text, (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 255), 1)
        
        # Show the frame
        cv2.imshow("AI Virtual Mouse", frame)
        
        # Check for keyboard input
        key_press = cv2.waitKey(1) & 0xFF
        
        if key_press == ord('q'):
            print("Exiting AI Virtual Mouse...")
            break
        elif key_press == ord('k'):
            keyboard_visible = not keyboard_visible
            status = "visible" if keyboard_visible else "hidden"
            print(f"✓ Virtual keyboard {status}")
        elif key_press == ord('v'):
            if voice:
                voice_active = not voice_active
                if voice_active:
                    voice.start_listening()
                    print("✓ Voice control started")
                else:
                    voice.stop_listening()
                    print("✓ Voice control stopped")
            else:
                print("✗ Voice control not available (install: pip install SpeechRecognition pyaudio)")
    
    # Release resources
    if voice and voice_active:
        print("Stopping voice control...")
        voice.stop_listening()
    
    if settings_gui:
        print("Closing settings GUI...")
        settings_gui.stop()
    
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
