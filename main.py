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
from hand_tracker import HandDetector
from mouse_controller import MouseController


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
    print("Press 'q' to quit.")
    
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
            
            # Mode 1: Only Index finger is up -> Move mouse
            if fingers[1] == 1 and fingers[2] == 0:  # Index up, Middle down
                # Get index finger tip position
                x, y = index_finger_tip[1], index_finger_tip[2]
                
                # Map webcam coordinates to screen coordinates
                screen_x, screen_y = mouse.mapCoordinates(
                    x, y, frame_width, frame_height,
                    padding_left=50, padding_right=50,
                    padding_top=50, padding_bottom=50
                )
                
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
                
                # Map webcam coordinates to screen coordinates
                screen_x, screen_y = mouse.mapCoordinates(
                    x, y, frame_width, frame_height,
                    padding_left=50, padding_right=50,
                    padding_top=50, padding_bottom=50
                )
                
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
        
        # Calculate and display FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display control instructions on the frame
        cv2.putText(frame, "Press 'q' to quit", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show the frame
        cv2.imshow("AI Virtual Mouse", frame)
        
        # Check for quit key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting AI Virtual Mouse...")
            break
    
    # Release resources
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
