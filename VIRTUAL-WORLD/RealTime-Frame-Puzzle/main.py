"""
================================================================================
                        REAL-TIME FRAME PUZZLE GAME
                Interactive Puzzle with Hand Gesture Control
================================================================================

Description:
    A real-time puzzle game that converts webcam feed or static photos into
    interactive puzzles. Solve puzzles using hand gestures with drag & drop
    functionality powered by computer vision and hand tracking.

Author: ANUBHAV YADAV
Date: March 10, 2026

Features:
    - Live webcam frame capture
    - Static image loading
    - Dynamic puzzle generation (3x3, 4x4, 5x5 grids)
    - Hand gesture-based drag & drop
    - Win condition detection
    - Real-time visual feedback

================================================================================
"""

import cv2
import numpy as np
import sys
import os
import time

# Add parent directory to path to access hand tracking module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FrameCapture:
    """
    Handles webcam capture, image loading, and frame preprocessing.
    """
    
    def __init__(self):
        """Initialize the FrameCapture with webcam configuration."""
        self.cap = None
        print("[INFO] FrameCapture initialized")
    
    def capture_from_webcam(self):
        """
        Capture a frame from the webcam with live preview.
        
        Returns:
            numpy.ndarray: Captured frame, or None if capture cancelled
        """
        try:
            # Initialize webcam
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                print("[ERROR] Could not access webcam!")
                return None
            
            print("\n[INFO] Webcam opened successfully")
            print("[INFO] Press SPACE to capture, ESC to exit")
            
            captured_frame = None
            
            while True:
                # Read frame from webcam
                ret, frame = self.cap.read()
                
                if not ret:
                    print("[ERROR] Failed to read frame from webcam")
                    break
                
                # Create display frame with instructions
                display_frame = frame.copy()
                
                # Add semi-transparent overlay for instructions
                overlay = display_frame.copy()
                cv2.rectangle(overlay, (10, 10), (630, 120), (0, 0, 0), -1)
                cv2.addWeighted(overlay, 0.7, display_frame, 0.3, 0, display_frame)
                
                # Add instruction text
                cv2.putText(display_frame, "WEBCAM CAPTURE MODE", 
                           (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cv2.putText(display_frame, "Press SPACE to capture frame", 
                           (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv2.putText(display_frame, "Press ESC to exit", 
                           (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Show the frame
                cv2.imshow("Webcam - Frame Capture", display_frame)
                
                # Wait for key press
                key = cv2.waitKey(1) & 0xFF
                
                if key == 32:  # SPACE key
                    captured_frame = frame.copy()
                    print("[SUCCESS] Frame captured!")
                    break
                elif key == 27:  # ESC key
                    print("[INFO] Capture cancelled by user")
                    break
            
            # Cleanup
            self.release()
            cv2.destroyAllWindows()
            
            return captured_frame
            
        except Exception as e:
            print(f"[ERROR] Exception during webcam capture: {e}")
            self.release()
            return None
    
    def load_from_file(self, filepath):
        """
        Load an image from a file.
        
        Args:
            filepath (str): Path to the image file
            
        Returns:
            numpy.ndarray: Loaded image, or None if loading fails
        """
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                print(f"[ERROR] File not found: {filepath}")
                return None
            
            # Load image
            image = cv2.imread(filepath)
            
            if image is None:
                print(f"[ERROR] Failed to load image from: {filepath}")
                return None
            
            print(f"[SUCCESS] Image loaded from: {filepath}")
            return image
            
        except Exception as e:
            print(f"[ERROR] Exception while loading file: {e}")
            return None
    
    def preprocess_frame(self, frame, target_size=(600, 600)):
        """
        Preprocess frame by resizing and adding padding to make it square.
        
        Args:
            frame (numpy.ndarray): Input frame
            target_size (tuple): Target dimensions (width, height)
            
        Returns:
            numpy.ndarray: Preprocessed frame
        """
        if frame is None:
            print("[ERROR] Cannot preprocess None frame")
            return None
        
        try:
            # Get original dimensions
            height, width = frame.shape[:2]
            target_w, target_h = target_size
            
            print(f"[INFO] Original frame size: {width}x{height}")
            
            # Calculate aspect ratio
            aspect_ratio = width / height
            
            # Calculate new dimensions maintaining aspect ratio
            if aspect_ratio > 1:  # Wider than tall
                new_width = target_w
                new_height = int(target_w / aspect_ratio)
            else:  # Taller than wide
                new_height = target_h
                new_width = int(target_h * aspect_ratio)
            
            # Resize frame
            resized = cv2.resize(frame, (new_width, new_height), 
                               interpolation=cv2.INTER_AREA)
            
            # Create canvas with padding
            canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
            
            # Calculate padding offsets to center the image
            y_offset = (target_h - new_height) // 2
            x_offset = (target_w - new_width) // 2
            
            # Place resized image on canvas
            canvas[y_offset:y_offset+new_height, 
                   x_offset:x_offset+new_width] = resized
            
            # Check brightness (optional quality check)
            gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            print(f"[INFO] Frame brightness: {brightness:.2f}")
            
            if brightness < 30:
                print("[WARNING] Frame is very dark, consider better lighting")
            elif brightness > 225:
                print("[WARNING] Frame is very bright, consider reducing lighting")
            
            print(f"[SUCCESS] Frame preprocessed to: {target_w}x{target_h}")
            
            return canvas
            
        except Exception as e:
            print(f"[ERROR] Exception during preprocessing: {e}")
            return None
    
    def release(self):
        """Release webcam resources."""
        if self.cap is not None:
            self.cap.release()
            print("[INFO] Webcam resources released")


def show_menu():
    """
    Display main menu and get user choice.
    
    Returns:
        str: User's choice ('W', 'F', or 'ESC')
    """
    # Create menu canvas
    menu = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Add title
    cv2.putText(menu, "REAL-TIME FRAME PUZZLE", 
                (130, 100), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 3)
    
    # Add decorative line
    cv2.line(menu, (100, 130), (700, 130), (0, 255, 255), 2)
    
    # Add menu options with styling
    cv2.putText(menu, "SELECT INPUT SOURCE:", 
                (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    # Option 1: Webcam
    cv2.rectangle(menu, (150, 240), (650, 290), (0, 255, 0), 2)
    cv2.putText(menu, "Press 'W' - Capture from Webcam", 
                (180, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Option 2: File
    cv2.rectangle(menu, (150, 310), (650, 360), (255, 165, 0), 2)
    cv2.putText(menu, "Press 'F' - Load from File", 
                (180, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
    
    # Option 3: Exit
    cv2.rectangle(menu, (150, 380), (650, 430), (0, 0, 255), 2)
    cv2.putText(menu, "Press 'ESC' - Exit Game", 
                (180, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Add footer
    cv2.putText(menu, "Author: ANUBHAV YADAV | March 2026", 
                (200, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 1)
    
    # Show menu
    cv2.imshow("Main Menu", menu)
    
    print("\n[MENU] Waiting for user input...")
    print("[MENU] Press 'W' for Webcam, 'F' for File, 'ESC' to Exit")
    
    # Wait for user input
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('w') or key == ord('W'):
            cv2.destroyAllWindows()
            return 'W'
        elif key == ord('f') or key == ord('F'):
            cv2.destroyAllWindows()
            return 'F'
        elif key == 27:  # ESC
            cv2.destroyAllWindows()
            return 'ESC'


def main():
    """
    Main entry point for the Real-Time Frame Puzzle game.
    """
    print("=" * 80)
    print("🧩 Real-Time Frame Puzzle - Starting...")
    print("=" * 80)
    
    # Show menu and get user choice
    choice = show_menu()
    
    if choice == 'ESC':
        print("\n[INFO] Exiting game. Goodbye!")
        return
    
    # Initialize frame capture
    frame_capture = FrameCapture()
    source_frame = None
    
    try:
        if choice == 'W':
            # Capture from webcam
            print("\n[INFO] Webcam capture mode selected")
            source_frame = frame_capture.capture_from_webcam()
            
        elif choice == 'F':
            # Load from file
            print("\n[INFO] File load mode selected")
            
            # For this implementation, use a test path or ask user
            # You can modify this to use a file dialog
            filepath = input("Enter image file path (or press Enter for demo): ").strip()
            
            if filepath == "":
                print("[INFO] No file path provided")
                # You could add a default test image path here
                print("[INFO] Please provide a valid image path to continue")
                return
            
            source_frame = frame_capture.load_from_file(filepath)
        
        # Check if frame was captured/loaded
        if source_frame is None:
            print("\n[ERROR] Failed to obtain source frame!")
            return
        
        # Preprocess the frame
        print("\n[INFO] Preprocessing frame...")
        processed_frame = frame_capture.preprocess_frame(source_frame, target_size=(600, 600))
        
        if processed_frame is None:
            print("[ERROR] Frame preprocessing failed!")
            return
        
        # Add visual feedback - green border
        display_frame = processed_frame.copy()
        cv2.rectangle(display_frame, (0, 0), (599, 599), (0, 255, 0), 5)
        
        # Add success message overlay
        cv2.rectangle(display_frame, (10, 10), (590, 80), (0, 255, 0), -1)
        cv2.putText(display_frame, "Frame Captured Successfully!", 
                   (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(display_frame, f"Dimensions: 600x600", 
                   (30, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        # Display the processed frame
        cv2.imshow("Puzzle Source Image", display_frame)
        
        print("\n" + "=" * 80)
        print("[SUCCESS] Frame ready for puzzle generation!")
        print(f"[INFO] Frame dimensions: 600x600 pixels")
        print("[INFO] Press any key to close...")
        print("=" * 80 + "\n")
        
        # Wait for key press
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # TODO: Implement puzzle generation from frame
        # TODO: Integrate hand gesture detection and tracking
        # TODO: Add drag & drop piece movement
        # TODO: Implement game loop with win condition
        # TODO: Add UI elements (timer, moves counter, difficulty selector)
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error in main: {e}")
        cv2.destroyAllWindows()
    
    finally:
        frame_capture.release()
        print("[INFO] Cleanup complete")


if __name__ == "__main__":
    main()
