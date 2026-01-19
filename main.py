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
    # Initialize webcam
    capture = cv2.VideoCapture(0)
    capture.set(3, 640)  # Set width
    capture.set(4, 480)  # Set height
    
    # Check if webcam opened successfully
    if not capture.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # Initialize hand detector and mouse controller
    detector = HandDetector(max_hands=1, detection_confidence=0.75, tracking_confidence=0.75)
    mouse = MouseController(smoothing_factor=5)
    
    # Variables for FPS calculation
    prev_time = 0
    
    # Variables for click detection
    click_performed = False
    click_cooldown_time = 0.5  # Cooldown period in seconds to prevent multiple clicks
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
                    padding_left=100, padding_right=100,
                    padding_top=100, padding_bottom=100
                )
                
                # Move the cursor
                mouse.moveCursor(screen_x, screen_y)
                
                # Draw a circle on the index finger tip for visual feedback
                cv2.circle(frame, (x, y), 15, (0, 255, 0), cv2.FILLED)
                
                # Reset click performed flag when in move mode
                click_performed = False
            
            # Mode 2: Index and Middle fingers are up -> Check for click
            elif fingers[1] == 1 and fingers[2] == 1:  # Both Index and Middle up
                # Calculate distance between index and middle finger tips
                distance = calculate_distance(index_finger_tip, middle_finger_tip)
                
                # Draw a line between the two fingertips for visual feedback
                cv2.line(frame, 
                        (index_finger_tip[1], index_finger_tip[2]), 
                        (middle_finger_tip[1], middle_finger_tip[2]), 
                        (255, 0, 255), 3)
                
                # Calculate midpoint for visual feedback
                mid_x = (index_finger_tip[1] + middle_finger_tip[1]) // 2
                mid_y = (index_finger_tip[2] + middle_finger_tip[2]) // 2
                cv2.circle(frame, (mid_x, mid_y), 10, (255, 0, 255), cv2.FILLED)
                
                # If fingers are close together, perform click
                # Distance threshold depends on hand size and camera distance
                click_threshold = 40  # pixels
                current_time = time.time()
                
                if distance < click_threshold:
                    # Check cooldown to prevent multiple rapid clicks
                    if not click_performed and (current_time - last_click_time > click_cooldown_time):
                        mouse.click(button='left')
                        print("Click performed!")
                        
                        # Visual feedback for click
                        cv2.circle(frame, (mid_x, mid_y), 15, (0, 255, 0), cv2.FILLED)
                        
                        # Set flags to prevent multiple clicks
                        click_performed = True
                        last_click_time = current_time
                else:
                    # Reset click flag when fingers are apart
                    click_performed = False
        
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
