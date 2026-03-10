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


class PuzzlePiece:
    """
    Represents a single puzzle piece with position and image data.
    """
    
    def __init__(self, piece_id, image, original_pos, current_pos, rect):
        """
        Initialize a puzzle piece.
        
        Args:
            piece_id (int): Unique identifier for the piece
            image (numpy.ndarray): Image data for this piece
            original_pos (tuple): Original (row, col) position
            current_pos (tuple): Current (row, col) position
            rect (tuple): Rendering rectangle (x, y, width, height)
        """
        self.id = piece_id
        self.image = image
        self.original_position = original_pos
        self.current_position = current_pos
        self.rect = rect  # (x, y, width, height)
    
    def is_correct_position(self):
        """
        Check if piece is in its correct position.
        
        Returns:
            bool: True if current position matches original position
        """
        return self.current_position == self.original_position


class PuzzleGrid:
    """
    Manages the puzzle grid, pieces, and rendering.
    """
    
    def __init__(self, source_image, grid_size=3):
        """
        Initialize the puzzle grid.
        
        Args:
            source_image (numpy.ndarray): 600x600 source image
            grid_size (int): Number of rows/columns (3, 4, or 5)
        """
        self.source_image = source_image
        self.grid_size = grid_size
        self.pieces = []
        self.piece_width = 600 // grid_size
        self.piece_height = 600 // grid_size
        self.canvas_size = 700
        self.offset = 50  # Padding for centering
        
        print(f"[INFO] PuzzleGrid initialized with {grid_size}×{grid_size} grid")
    
    def create_pieces(self):
        """
        Split source image into grid pieces and create PuzzlePiece objects.
        """
        print(f"\n[INFO] Creating puzzle pieces...")
        print(f"[INFO] Grid size: {self.grid_size}×{self.grid_size}")
        print(f"[INFO] Piece dimensions: {self.piece_width}×{self.piece_height} pixels")
        
        piece_id = 1
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Calculate pixel coordinates for slicing
                y1 = row * self.piece_height
                y2 = y1 + self.piece_height
                x1 = col * self.piece_width
                x2 = x1 + self.piece_width
                
                # Extract piece from source image
                piece_image = self.source_image[y1:y2, x1:x2].copy()
                
                # Calculate rendering position (with offset for centering)
                rect_x = self.offset + col * self.piece_width
                rect_y = self.offset + row * self.piece_height
                rect = (rect_x, rect_y, self.piece_width, self.piece_height)
                
                # Create puzzle piece
                piece = PuzzlePiece(
                    piece_id=piece_id,
                    image=piece_image,
                    original_pos=(row, col),
                    current_pos=(row, col),
                    rect=rect
                )
                
                self.pieces.append(piece)
                
                print(f"[DEBUG] Piece {piece_id}: pos({row},{col}), rect{rect}")
                
                piece_id += 1
        
        total_pieces = len(self.pieces)
        print(f"[SUCCESS] Created {total_pieces} puzzle pieces!")
        
        return total_pieces
    
    def draw_grid(self, show_numbers=True, show_info=True):
        """
        Render the puzzle grid with all pieces.
        
        Args:
            show_numbers (bool): Display piece numbers for debugging
            show_info (bool): Show grid information overlay
            
        Returns:
            numpy.ndarray: Rendered canvas with puzzle
        """
        # Create black canvas
        canvas = np.zeros((self.canvas_size, self.canvas_size, 3), dtype=np.uint8)
        
        # Draw all pieces
        for piece in self.pieces:
            x, y, w, h = piece.rect
            
            # Place piece image on canvas
            canvas[y:y+h, x:x+w] = piece.image
            
            # Draw piece border (white)
            cv2.rectangle(canvas, (x, y), (x+w, y+h), (255, 255, 255), 2)
            
            # Optionally show piece numbers
            if show_numbers:
                # Add piece number in top-left corner
                cv2.putText(canvas, str(piece.id), 
                           (x + 5, y + 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 255), 2)
        
        # Draw outer border around entire puzzle
        border_x1 = self.offset
        border_y1 = self.offset
        border_x2 = self.offset + (self.grid_size * self.piece_width)
        border_y2 = self.offset + (self.grid_size * self.piece_height)
        cv2.rectangle(canvas, (border_x1, border_y1), (border_x2, border_y2), 
                     (0, 255, 0), 3)
        
        # Add grid information overlay
        if show_info:
            difficulty_map = {3: "EASY", 4: "MEDIUM", 5: "HARD"}
            color_map = {3: (0, 255, 0), 4: (0, 255, 255), 5: (0, 0, 255)}
            
            difficulty = difficulty_map.get(self.grid_size, "CUSTOM")
            color = color_map.get(self.grid_size, (255, 255, 255))
            
            # Info panel at bottom
            info_y = self.canvas_size - 40
            cv2.putText(canvas, f"{self.grid_size}x{self.grid_size} Grid | {len(self.pieces)} Pieces | {difficulty}", 
                       (50, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return canvas
    
    def get_piece_info(self):
        """
        Get information about the puzzle grid.
        
        Returns:
            dict: Dictionary with grid statistics
        """
        info = {
            'grid_size': self.grid_size,
            'total_pieces': len(self.pieces),
            'piece_width': self.piece_width,
            'piece_height': self.piece_height,
            'canvas_size': self.canvas_size
        }
        
        print("\n" + "=" * 60)
        print("PUZZLE GRID INFORMATION")
        print("=" * 60)
        print(f"Grid Size:      {info['grid_size']}×{info['grid_size']}")
        print(f"Total Pieces:   {info['total_pieces']}")
        print(f"Piece Size:     {info['piece_width']}×{info['piece_height']} pixels")
        print(f"Canvas Size:    {info['canvas_size']}×{info['canvas_size']} pixels")
        print("=" * 60 + "\n")
        
        return info


def select_difficulty():
    """
    Display difficulty selection menu and get user's choice.
    
    Returns:
        int: Selected grid size (3, 4, or 5), or None if cancelled
    """
    # Create difficulty menu canvas
    menu = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # Add title
    cv2.putText(menu, "SELECT DIFFICULTY", 
                (200, 100), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 255), 3)
    
    # Add decorative line
    cv2.line(menu, (100, 130), (700, 130), (0, 255, 255), 2)
    
    # Add instructions
    cv2.putText(menu, "Choose puzzle grid size:", 
                (180, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    # Option 1: Easy (3×3)
    cv2.rectangle(menu, (150, 220), (650, 280), (0, 255, 0), 3)
    cv2.putText(menu, "Press '3' - EASY (3x3 Grid = 9 pieces)", 
                (180, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Option 2: Medium (4×4)
    cv2.rectangle(menu, (150, 300), (650, 360), (0, 255, 255), 3)
    cv2.putText(menu, "Press '4' - MEDIUM (4x4 Grid = 16 pieces)", 
                (180, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    # Option 3: Hard (5×5)
    cv2.rectangle(menu, (150, 380), (650, 440), (0, 0, 255), 3)
    cv2.putText(menu, "Press '5' - HARD (5x5 Grid = 25 pieces)", 
                (180, 415), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Option 4: Back
    cv2.rectangle(menu, (150, 460), (650, 510), (128, 128, 128), 2)
    cv2.putText(menu, "Press 'ESC' - Go Back", 
                (180, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (128, 128, 128), 2)
    
    # Add footer
    cv2.putText(menu, "Higher difficulty = More pieces = Harder puzzle", 
                (150, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # Show menu
    cv2.imshow("Difficulty Selection", menu)
    
    print("\n[MENU] Select difficulty level...")
    print("[MENU] Press '3' (Easy), '4' (Medium), '5' (Hard), or 'ESC' (Back)")
    
    # Wait for user input
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('3'):
            cv2.destroyAllWindows()
            print("[INFO] Easy mode selected (3×3)")
            return 3
        elif key == ord('4'):
            cv2.destroyAllWindows()
            print("[INFO] Medium mode selected (4×4)")
            return 4
        elif key == ord('5'):
            cv2.destroyAllWindows()
            print("[INFO] Hard mode selected (5×5)")
            return 5
        elif key == 27:  # ESC
            cv2.destroyAllWindows()
            print("[INFO] Difficulty selection cancelled")
            return None


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
        
        # Display the processed frame briefly
        cv2.imshow("Puzzle Source Image", display_frame)
        
        print("\n" + "=" * 80)
        print("[SUCCESS] Frame ready for puzzle generation!")
        print(f"[INFO] Frame dimensions: 600x600 pixels")
        print("[INFO] Press any key to continue...")
        print("=" * 80 + "\n")
        
        # Wait for key press
        cv2.waitKey(2000)  # Show for 2 seconds
        cv2.destroyAllWindows()
        
        # ✅ COMMIT 3: Puzzle Grid Creation
        # Select difficulty level
        grid_size = select_difficulty()
        
        if grid_size is None:
            print("[INFO] Returning to main menu...")
            return
        
        # Create puzzle grid
        print("\n[INFO] Initializing puzzle grid...")
        puzzle = PuzzleGrid(processed_frame, grid_size=grid_size)
        
        # Create puzzle pieces by splitting the image
        total_pieces = puzzle.create_pieces()
        
        # Get and display puzzle information
        puzzle_info = puzzle.get_piece_info()
        
        # Draw the initial puzzle grid (unsolved state)
        print("[INFO] Rendering puzzle grid...")
        puzzle_canvas = puzzle.draw_grid(show_numbers=True, show_info=True)
        
        # Display the puzzle grid
        cv2.imshow("Puzzle Grid - Unsolved", puzzle_canvas)
        
        print("\n" + "=" * 80)
        print("[SUCCESS] Puzzle grid created successfully!")
        print(f"[INFO] Grid: {grid_size}×{grid_size} | Pieces: {total_pieces} | Size: {puzzle.piece_width}×{puzzle.piece_height}px")
        print("[INFO] Press any key to continue...")
        print("=" * 80 + "\n")
        
        # Wait for key press (show for at least 3 seconds)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        
        # TODO: Implement puzzle shuffling logic
        # TODO: Integrate hand gesture detection and tracking
        # TODO: Add drag & drop piece movement
        # TODO: Implement game loop with win condition
        # TODO: Add UI elements (timer, moves counter)
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error in main: {e}")
        cv2.destroyAllWindows()
    
    finally:
        frame_capture.release()
        print("[INFO] Cleanup complete")


if __name__ == "__main__":
    main()
