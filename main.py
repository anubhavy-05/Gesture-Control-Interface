"""
AI Virtual Mouse - Main Entry Point
Control your mouse cursor using hand gestures captured through your webcam.

Gestures:
- Index finger up: Move mouse cursor
- Index + Middle fingers up (close together): Perform left click
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
    click_performed = False
    click_cooldown_time = 0.3  # Cooldown period in seconds to prevent multiple clicks
    last_click_time = 0
    
    # Frame dimensions (will be updated when first frame is captured)
    frame_width = 640
    frame_height = 480
    
    print("AI Virtual Mouse Started!")
    print("Gestures:")
    print("  - Index finger up: Move mouse")
    print("  - Index + Middle fingers up (close together): Click")
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
            # Landmark 8: Index finger tip
            # Landmark 12: Middle finger tip
            index_finger_tip = landmark_list[8]
            middle_finger_tip = landmark_list[12]
            
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
                
                # Reset click performed flag when in move mode
                click_performed = False
            
            # Mode 2: Index and Middle fingers are up -> Check for click
            elif fingers[1] == 1 and fingers[2] == 1:  # Both Index and Middle up
                # Calculate distance between index and middle finger tips
                distance = calculate_distance(index_finger_tip, middle_finger_tip)
                
                # Calculate midpoint for visual feedback
                mid_x = (index_finger_tip[1] + middle_finger_tip[1]) // 2
                mid_y = (index_finger_tip[2] + middle_finger_tip[2]) // 2
                
                # Display click mode indicator
                cv2.putText(frame, "CLICK MODE", (10, 120), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                
                # Display distance for debugging
                cv2.putText(frame, f"Distance: {int(distance)}", (10, 150), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                
                # Draw a line between the two fingertips for visual feedback
                cv2.line(frame, 
                        (index_finger_tip[1], index_finger_tip[2]), 
                        (middle_finger_tip[1], middle_finger_tip[2]), 
                        (255, 0, 255), 3)
                
                cv2.circle(frame, (mid_x, mid_y), 10, (255, 0, 255), cv2.FILLED)
                
                # If fingers are close together, perform click
                # Distance threshold depends on hand size and camera distance
                click_threshold = 50  # Increased threshold for easier triggering
                current_time = time.time()
                
                if distance < click_threshold:
                    # Visual feedback - fingers are close enough
                    cv2.putText(frame, "CLICKING!", (10, 180), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.circle(frame, (mid_x, mid_y), 20, (0, 255, 0), cv2.FILLED)
                    
                    # Check cooldown to prevent multiple rapid clicks
                    if not click_performed and (current_time - last_click_time > click_cooldown_time):
                        try:
                            mouse.click(button='left')
                            print(f"✓ Click performed! Distance: {int(distance)}px")
                            
                            # Set flags to prevent multiple clicks
                            click_performed = True
                            last_click_time = current_time
                        except Exception as e:
                            print(f"Error clicking: {e}")
                else:
                    # Reset click flag when fingers are apart
                    click_performed = False
                    cv2.putText(frame, "Bring fingers closer", (10, 180), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
        
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
