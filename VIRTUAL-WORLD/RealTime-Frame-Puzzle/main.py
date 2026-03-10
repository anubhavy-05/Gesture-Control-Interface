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
import random

# Add parent directory to path to access hand tracking module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import hand tracking module with error handling
try:
    from hand_tracker import HandDetector
    HAND_TRACKING_AVAILABLE = True
    print("[INFO] HandDetector imported successfully")
except ImportError as e:
    print(f"[WARNING] HandDetector not found: {e}")
    print("[WARNING] Hand tracking will be unavailable. Keyboard fallback mode only.")
    HAND_TRACKING_AVAILABLE = False
    HandDetector = None


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
    
    def draw_grid(self, show_numbers=True, show_info=True, show_state=True):
        """
        Render the puzzle grid with all pieces.
        
        Args:
            show_numbers (bool): Display piece numbers for debugging
            show_info (bool): Show grid information overlay
            show_state (bool): Show puzzle state (SHUFFLED/SOLVED)
            
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
        
        # Check if puzzle is solved
        puzzle_solved = self.is_solved()
        
        # Draw outer border with color based on state
        border_x1 = self.offset
        border_y1 = self.offset
        border_x2 = self.offset + (self.grid_size * self.piece_width)
        border_y2 = self.offset + (self.grid_size * self.piece_height)
        
        # Change border color based on state
        border_color = (0, 255, 0) if puzzle_solved else (0, 0, 255)  # Green if solved, Red if shuffled
        cv2.rectangle(canvas, (border_x1, border_y1), (border_x2, border_y2), 
                     border_color, 3)
        
        # Add state indicator in top-left
        if show_state:
            state_text = "STATUS: SOLVED" if puzzle_solved else "STATUS: SHUFFLED"
            state_color = (0, 255, 0) if puzzle_solved else (0, 0, 255)
            
            # Add semi-transparent background for status
            overlay = canvas.copy()
            cv2.rectangle(overlay, (5, 5), (250, 35), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, canvas, 0.3, 0, canvas)
            
            cv2.putText(canvas, state_text, 
                       (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, state_color, 2)
        
        # Add grid information overlay
        if show_info:
            difficulty_map = {3: "EASY", 4: "MEDIUM", 5: "HARD"}
            color_map = {3: (0, 255, 0), 4: (0, 255, 255), 5: (0, 0, 255)}
            
            difficulty = difficulty_map.get(self.grid_size, "CUSTOM")
            color = color_map.get(self.grid_size, (255, 255, 255))
            
            # Info panel at bottom
            info_y = self.canvas_size - 40
            status_text = "SOLVED!" if puzzle_solved else "SHUFFLED"
            cv2.putText(canvas, f"{self.grid_size}x{self.grid_size} Grid | {len(self.pieces)} Pieces | {difficulty} | {status_text}", 
                       (40, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
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
    
    def shuffle_pieces(self):
        """
        Shuffle puzzle pieces randomly using Fisher-Yates algorithm.
        Ensures puzzle is solvable and not in solved state.
        
        Returns:
            dict: Shuffle statistics
        """
        print("\n[INFO] Shuffling puzzle...")
        print("[INFO] Performing random piece shuffling...")
        
        # Store original positions for comparison
        original_positions = [piece.current_position for piece in self.pieces]
        
        # Generate all possible positions
        all_positions = [(r, c) for r in range(self.grid_size) 
                        for c in range(self.grid_size)]
        
        # Shuffle positions using Fisher-Yates algorithm
        max_attempts = 10
        attempt = 0
        pieces_moved = 0
        
        while attempt < max_attempts:
            # Create shuffled copy of positions
            shuffled_positions = all_positions.copy()
            random.shuffle(shuffled_positions)
            
            # Count how many pieces would move
            moves = sum(1 for i, pos in enumerate(shuffled_positions) 
                       if pos != original_positions[i])
            
            # Ensure at least 70% of pieces are moved
            min_moves = int(len(self.pieces) * 0.7)
            
            if moves >= min_moves:
                pieces_moved = moves
                break
            
            attempt += 1
        
        # Apply the shuffle
        swap_count = 0
        for i, piece in enumerate(self.pieces):
            new_pos = shuffled_positions[i]
            old_pos = piece.current_position
            
            if new_pos != old_pos:
                print(f"[DEBUG] Piece {piece.id} moved from {old_pos} to {new_pos}")
                swap_count += 1
            
            # Update piece position
            piece.current_position = new_pos
            
            # Update rect for rendering
            new_row, new_col = new_pos
            piece.rect = (
                self.offset + new_col * self.piece_width,
                self.offset + new_row * self.piece_height,
                self.piece_width,
                self.piece_height
            )
        
        # Validate solvability
        is_solvable = self.validate_solvability()
        
        print(f"[SUCCESS] Puzzle shuffled successfully!")
        print(f"[INFO] Total swaps performed: {swap_count}")
        print(f"[INFO] Pieces moved: {pieces_moved} out of {len(self.pieces)}")
        print(f"[INFO] Puzzle is solvable: {is_solvable}")
        
        # Return shuffle statistics
        stats = {
            'swaps': swap_count,
            'pieces_moved': pieces_moved,
            'total_pieces': len(self.pieces),
            'solvable': is_solvable,
            'attempts': attempt + 1
        }
        
        return stats
    
    def is_solved(self):
        """
        Check if puzzle is in solved state.
        
        Returns:
            bool: True if all pieces are in correct positions
        """
        correct_count = 0
        incorrect_count = 0
        
        for piece in self.pieces:
            if piece.is_correct_position():
                correct_count += 1
            else:
                incorrect_count += 1
        
        is_complete = (incorrect_count == 0)
        
        print(f"[DEBUG] Puzzle check - Correct: {correct_count}, Incorrect: {incorrect_count}")
        
        return is_complete
    
    def validate_solvability(self):
        """
        Validate that the puzzle is solvable.
        
        For swap-based puzzles, all permutations are solvable.
        This method ensures the puzzle is not in a trivial state.
        
        Returns:
            bool: True if puzzle is solvable
        """
        # For this type of puzzle where we can swap any pieces,
        # all configurations are solvable
        # We just need to ensure it's not in solved state
        
        not_solved = not all(piece.is_correct_position() for piece in self.pieces)
        
        return not_solved


class GestureController:
    """
    Manages hand gesture detection and tracking for puzzle interaction.
    """
    
    def __init__(self, puzzle_grid):
        """
        Initialize gesture controller with puzzle grid reference.
        
        Args:
            puzzle_grid (PuzzleGrid): Reference to the puzzle grid
        """
        self.puzzle_grid = puzzle_grid
        self.hand_detector = None
        self.webcam = None
        self.frame_width = 640
        self.frame_height = 480
        self.puzzle_bounds = (0, 0, 700, 700)  # Puzzle area bounds
        self.current_finger_pos = None
        self.pinch_state = False
        self.last_landmarks = None
        
        print("[INFO] GestureController initialized")
    
    def start_webcam(self):
        """
        Open webcam for hand tracking.
        
        Returns:
            bool: True if webcam opened successfully
        """
        if not HAND_TRACKING_AVAILABLE:
            print("[ERROR] Hand tracking not available!")
            return False
        
        try:
            # Initialize hand detector
            self.hand_detector = HandDetector(max_hands=1, detection_confidence=0.7)
            print("[INFO] HandDetector initialized")
            
            # Open webcam
            self.webcam = cv2.VideoCapture(0)
            
            if not self.webcam.isOpened():
                print("[ERROR] Could not open webcam for hand tracking!")
                return False
            
            # Set webcam resolution
            self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            
            print(f"[INFO] Webcam opened for hand tracking ({self.frame_width}x{self.frame_height})")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to start webcam: {e}")
            return False
    
    def get_hand_frame(self):
        """
        Read frame from webcam and detect hands.
        
        Returns:
            tuple: (frame, landmarks) or (None, None) if failed
        """
        if self.webcam is None or not self.webcam.isOpened():
            return None, None
        
        try:
            ret, frame = self.webcam.read()
            
            if not ret:
                return None, None
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect hands
            frame, landmarks = self.hand_detector.find_hands(frame, draw=True)
            
            # Store landmarks for later use
            self.last_landmarks = landmarks
            
            return frame, landmarks
            
        except Exception as e:
            print(f"[ERROR] Error reading frame: {e}")
            return None, None
    
    def get_finger_position(self, landmarks):
        """
        Get index finger tip coordinates.
        
        Args:
            landmarks (list): Hand landmarks from MediaPipe
            
        Returns:
            tuple: (x, y) coordinates of index finger tip, or None
        """
        if not landmarks or len(landmarks) == 0:
            return None
        
        try:
            # Index finger tip is landmark 8
            hand_data = landmarks[0]
            if 'lmList' in hand_data and len(hand_data['lmList']) > 8:
                landmark = hand_data['lmList'][8]
                return (landmark[0], landmark[1])
            
            return None
            
        except Exception as e:
            print(f"[DEBUG] Error getting finger position: {e}")
            return None
    
    def is_pinching(self, landmarks):
        """
        Check if thumb and index finger are close (pinch gesture).
        
        Args:
            landmarks (list): Hand landmarks from MediaPipe
            
        Returns:
            bool: True if pinching (distance < 30px)
        """
        if not landmarks or len(landmarks) == 0:
            return False
        
        try:
            hand_data = landmarks[0]
            if 'lmList' in hand_data:
                lm_list = hand_data['lmList']
                
                # Thumb tip (4) and index finger tip (8)
                if len(lm_list) > 8:
                    thumb_tip = lm_list[4]
                    index_tip = lm_list[8]
                    
                    # Calculate distance
                    distance = np.sqrt(
                        (thumb_tip[0] - index_tip[0])**2 + 
                        (thumb_tip[1] - index_tip[1])**2
                    )
                    
                    self.pinch_state = distance < 30
                    return self.pinch_state
            
            return False
            
        except Exception as e:
            print(f"[DEBUG] Error checking pinch: {e}")
            return False
    
    def map_to_puzzle_coords(self, hand_x, hand_y):
        """
        Map webcam coordinates to puzzle grid coordinates.
        
        Args:
            hand_x (int): X coordinate from webcam (0-640)
            hand_y (int): Y coordinate from webcam (0-480)
            
        Returns:
            tuple: (puzzle_x, puzzle_y) or None if outside bounds
        """
        if hand_x is None or hand_y is None:
            return None
        
        # Map webcam coords (640x480) to puzzle coords (700x700)
        # Scale down slightly to account for ratio difference
        puzzle_x = int(hand_x * (700 / 640))
        puzzle_y = int(hand_y * (700 / 480))
        
        # Check if within puzzle bounds
        if 0 <= puzzle_x < 700 and 0 <= puzzle_y < 700:
            return (puzzle_x, puzzle_y)
        
        return None
    
    def get_piece_under_finger(self, puzzle_coords):
        """
        Get puzzle piece at the given puzzle coordinates.
        
        Args:
            puzzle_coords (tuple): (x, y) coordinates in puzzle space
            
        Returns:
            PuzzlePiece: Piece at position, or None
        """
        if puzzle_coords is None:
            return None
        
        puzzle_x, puzzle_y = puzzle_coords
        
        # Check each piece to see if coords fall within its rect
        for piece in self.puzzle_grid.pieces:
            x, y, w, h = piece.rect
            if x <= puzzle_x < (x + w) and y <= puzzle_y < (y + h):
                return piece
        
        return None
    
    def draw_hand_overlay(self, frame):
        """
        Draw hand tracking information overlay on frame.
        
        Args:
            frame (numpy.ndarray): Webcam frame
            
        Returns:
            numpy.ndarray: Frame with overlay
        """
        if frame is None:
            return frame
        
        overlay = frame.copy()
        
        # Add semi-transparent info panel
        cv2.rectangle(overlay, (0, 0), (640, 60), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Add title
        cv2.putText(frame, "HAND TRACKING", 
                   (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Show hand detection status
        hand_status = "Detected" if self.last_landmarks else "No Hand"
        color = (0, 255, 0) if self.last_landmarks else (0, 0, 255)
        cv2.putText(frame, f"Hand: {hand_status}", 
                   (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Show pinch status
        if self.last_landmarks:
            pinch_text = "PINCH!" if self.pinch_state else "Open"
            pinch_color = (0, 0, 255) if self.pinch_state else (0, 255, 0)
            cv2.putText(frame, f"Gesture: {pinch_text}", 
                       (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, pinch_color, 1)
            
            # Draw finger position indicator
            if self.current_finger_pos:
                color = (0, 0, 255) if self.pinch_state else (0, 255, 0)
                cv2.circle(frame, self.current_finger_pos, 15, color, 3)
                cv2.circle(frame, self.current_finger_pos, 5, color, -1)
        
        return frame
    
    def release(self):
        """Release webcam and cleanup resources."""
        if self.webcam is not None:
            self.webcam.release()
            print("[INFO] Gesture controller webcam released")


def create_split_screen_display(puzzle_canvas, hand_frame, piece_under_finger=None, 
                                  finger_pos=None, pinch_state=False, fps=0):
    """
    Create split-screen display with puzzle and hand tracking.
    
    Args:
        puzzle_canvas (numpy.ndarray): Rendered puzzle (700x700)
        hand_frame (numpy.ndarray): Webcam feed with hand tracking (640x480)
        piece_under_finger (PuzzlePiece): Currently highlighted piece
        finger_pos (tuple): Current finger position
        pinch_state (bool): Whether pinch gesture is active
        fps (float): Current FPS
        
    Returns:
        numpy.ndarray: Combined display (1340x700)
    """
    # Create canvas for split-screen display
    display = np.zeros((700, 1340, 3), dtype=np.uint8)
    
    # Place puzzle on left side (700x700)
    display[0:700, 0:700] = puzzle_canvas
    
    # Resize and place hand frame on right side
    if hand_frame is not None:
        # Resize hand frame to fit (640x480 → 640x480, centered in 640x700)
        hand_display = np.zeros((700, 640, 3), dtype=np.uint8)
        y_offset = (700 - 480) // 2
        hand_display[y_offset:y_offset+480, 0:640] = hand_frame
        display[0:700, 700:1340] = hand_display
    
    # Add separator line
    cv2.line(display, (700, 0), (700, 700), (0, 255, 255), 3)
    
    # Add section labels
    cv2.putText(display, "PUZZLE GRID", 
                (250, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(display, "HAND TRACKING", 
                (900, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
    
    # Add instructions at bottom
    overlay = display.copy()
    cv2.rectangle(overlay, (0, 650), (1340, 700), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.8, display, 0.2, 0, display)
    
    instructions = "Point to select | Pinch to grab | Move to drag | Q=Quit"
    cv2.putText(display, instructions, 
                (320, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Add piece info if piece is under finger
    if piece_under_finger:
        info_text = f"Piece {piece_under_finger.id} selected"
        cv2.putText(display, info_text, 
                   (20, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Add FPS counter
    if fps > 0:
        cv2.putText(display, f"FPS: {fps:.1f}", 
                   (1230, 680), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    
    return display


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


def show_shuffle_confirmation(puzzle_canvas, shuffle_stats):
    """
    Display shuffle confirmation and get user's choice.
    
    Args:
        puzzle_canvas (numpy.ndarray): Rendered puzzle canvas
        shuffle_stats (dict): Statistics from shuffle operation
        
    Returns:
        str: User's choice ('START', 'SHUFFLE', or 'QUIT')
    """
    # Create confirmation overlay on puzzle canvas
    display = puzzle_canvas.copy()
    
    # Add semi-transparent overlay panel
    overlay = display.copy()
    panel_height = 200
    panel_y = (700 - panel_height) // 2
    cv2.rectangle(overlay, (50, panel_y), (650, panel_y + panel_height), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.85, display, 0.15, 0, display)
    
    # Add title
    cv2.putText(display, "PUZZLE SHUFFLED!", 
                (150, panel_y + 40), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 2)
    
    # Add shuffle statistics
    pieces_moved = shuffle_stats.get('pieces_moved', 0)
    total_pieces = shuffle_stats.get('total_pieces', 0)
    
    cv2.putText(display, f"Pieces Moved: {pieces_moved}/{total_pieces}", 
                (180, panel_y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Add decorative line
    cv2.line(display, (100, panel_y + 100), (600, panel_y + 100), (0, 255, 255), 2)
    
    # Add instructions
    cv2.putText(display, "SPACE - Start Game", 
                (150, panel_y + 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(display, "ESC - Re-shuffle  |  Q - Quit", 
                (150, panel_y + 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    
    # Show the confirmation window
    cv2.imshow("Puzzle - Shuffled (READY TO PLAY)", display)
    
    print("\n[CONFIRM] Puzzle shuffled! What would you like to do?")
    print("[CONFIRM] Press SPACE to start, ESC to re-shuffle, Q to quit")
    
    # Wait for user input
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE
            cv2.destroyAllWindows()
            print("[INFO] Starting game...")
            return 'START'
        elif key == 27:  # ESC
            cv2.destroyAllWindows()
            print("[INFO] Re-shuffling puzzle...")
            return 'SHUFFLE'
        elif key == ord('q') or key == ord('Q'):
            cv2.destroyAllWindows()
            print("[INFO] Quitting to main menu...")
            return 'QUIT'


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
        puzzle_canvas = puzzle.draw_grid(show_numbers=True, show_info=True, show_state=False)
        
        # Display the puzzle grid briefly
        cv2.imshow("Puzzle Grid - Unsolved", puzzle_canvas)
        
        print("\n" + "=" * 80)
        print("[SUCCESS] Puzzle grid created successfully!")
        print(f"[INFO] Grid: {grid_size}×{grid_size} | Pieces: {total_pieces} | Size: {puzzle.piece_width}×{puzzle.piece_height}px")
        print("[INFO] Showing unsolved grid for 2 seconds...")
        print("=" * 80 + "\n")
        
        # Wait for key press (show for 2 seconds)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
        
        # ✅ COMMIT 4: Puzzle Shuffling Logic
        shuffle_choice = 'SHUFFLE'
        
        while shuffle_choice == 'SHUFFLE':
            # Shuffle the puzzle
            print("\n" + "=" * 80)
            print("SHUFFLING PUZZLE")
            print("=" * 80)
            
            shuffle_stats = puzzle.shuffle_pieces()
            
            # Verify puzzle is not solved
            is_solved_check = puzzle.is_solved()
            print(f"[INFO] Puzzle is solved: {is_solved_check} {'✗ (Good!)' if not is_solved_check else '✓ (Need to re-shuffle)'}")
            
            # If somehow still solved, shuffle again
            if is_solved_check:
                print("[WARNING] Puzzle is still in solved state, re-shuffling...")
                continue
            
            print("=" * 80 + "\n")
            
            # Draw the shuffled puzzle
            print("[INFO] Rendering shuffled puzzle...")
            shuffled_canvas = puzzle.draw_grid(show_numbers=True, show_info=True, show_state=True)
            
            # Add shuffle statistics overlay
            overlay = shuffled_canvas.copy()
            cv2.rectangle(overlay, (10, 650), (350, 690), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, shuffled_canvas, 0.3, 0, shuffled_canvas)
            
            cv2.putText(shuffled_canvas, 
                       f"Moved: {shuffle_stats['pieces_moved']}/{shuffle_stats['total_pieces']} pieces", 
                       (15, 675), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Display shuffled puzzle
            cv2.imshow("Puzzle - Shuffled", shuffled_canvas)
            
            print("\n" + "=" * 80)
            print("[SUCCESS] Puzzle shuffled and ready to play!")
            print(f"[INFO] Shuffle Statistics:")
            print(f"  - Pieces moved: {shuffle_stats['pieces_moved']}/{shuffle_stats['total_pieces']}")
            print(f"  - Total swaps: {shuffle_stats['swaps']}")
            print(f"  - Solvable: {shuffle_stats['solvable']}")
            print("[INFO] Showing shuffled puzzle for 3 seconds...")
            print("=" * 80 + "\n")
            
            # Show for 3 seconds
            cv2.waitKey(3000)
            
            # Show confirmation and get user choice
            shuffle_choice = show_shuffle_confirmation(shuffled_canvas, shuffle_stats)
            
            if shuffle_choice == 'QUIT':
                print("[INFO] Returning to main menu...")
                cv2.destroyAllWindows()
                return
        
        # If we get here, user chose 'START'
        print("\n" + "=" * 80)
        print("GAME STARTING")
        print("=" * 80)
        print("[INFO] Hand gesture controls will be implemented in Commit 5")
        print("[INFO] For now, press any key to exit...")
        print("=" * 80 + "\n")
        
        cv2.imshow("Puzzle - Game Mode", shuffled_canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # TODO: Integrate hand gesture detection and tracking (Commit 5)
        # TODO: Add piece selection & snap mechanism (Commit 6)
        # TODO: Add drag & drop piece movement (Commit 7)
        # TODO: Add piece swapping logic (Commit 8)
        # TODO: Implement game loop with win condition (Commit 9)
        # TODO: Add UI elements (timer, moves counter, difficulty selector) (Commit 10)
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error in main: {e}")
        cv2.destroyAllWindows()
    
    finally:
        frame_capture.release()
        print("[INFO] Cleanup complete")


if __name__ == "__main__":
    main()
