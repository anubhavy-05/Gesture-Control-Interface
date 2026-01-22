"""
Virtual Keyboard Module
Displays a semi-transparent QWERTY keyboard overlay on the video feed.
Supports hover detection and key typing using pyautogui.
"""

import cv2
import numpy as np
import pyautogui
import time


class VirtualKeyboard:
    """
    A class to create and manage a virtual on-screen keyboard overlay.
    """

    def __init__(self, frame_width=640, frame_height=480):
        """
        Initialize the VirtualKeyboard.
        
        Args:
            frame_width (int): Width of the video frame.
            frame_height (int): Height of the video frame.
        """
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Define keyboard layout (QWERTY)
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACK'],
            ['SPACE', 'ENTER']
        ]
        
        # Keyboard positioning and sizing
        self.keyboard_y_offset = int(frame_height * 0.55)  # Start at 55% of frame height
        self.key_width = 50
        self.key_height = 50
        self.key_margin = 10
        
        # Colors (BGR format)
        self.key_color = (50, 50, 50)  # Dark gray
        self.key_hover_color = (100, 200, 100)  # Green when hovering
        self.key_pressed_color = (0, 255, 0)  # Bright green when pressed
        self.text_color = (255, 255, 255)  # White text
        
        # Transparency settings
        self.keyboard_alpha = 0.6  # Semi-transparent overlay
        
        # Hover tracking
        self.hover_start_time = None
        self.current_hover_key = None
        self.hover_threshold = 1.0  # Seconds to hover before typing
        self.last_typed_key = None
        self.last_typed_time = 0
        self.typing_cooldown = 0.5  # Cooldown between key presses
        
        # Build key rectangles
        self.key_rectangles = self._build_key_rectangles()
    
    def _build_key_rectangles(self):
        """
        Build rectangles for each key based on layout.
        
        Returns:
            dict: Dictionary mapping key names to their (x, y, width, height) rectangles.
        """
        key_rects = {}
        y_pos = self.keyboard_y_offset
        
        for row_idx, row in enumerate(self.keys):
            # Calculate total width of this row to center it
            row_width = len(row) * self.key_width + (len(row) - 1) * self.key_margin
            
            # Special width for SPACE and BACK keys
            if 'SPACE' in row:
                row_width = 400  # SPACE takes most of the width
            
            x_pos = (self.frame_width - row_width) // 2
            
            for key in row:
                if key == 'SPACE':
                    # SPACE key is extra wide
                    width = 250
                elif key == 'BACK':
                    # BACK key is wider
                    width = 80
                elif key == 'ENTER':
                    # ENTER key is wider
                    width = 120
                else:
                    width = self.key_width
                
                key_rects[key] = (x_pos, y_pos, width, self.key_height)
                x_pos += width + self.key_margin
            
            y_pos += self.key_height + self.key_margin
        
        return key_rects
    
    def draw_keyboard(self, frame):
        """
        Draw the virtual keyboard overlay on the frame.
        
        Args:
            frame (numpy.ndarray): The video frame to draw on.
        
        Returns:
            numpy.ndarray: Frame with keyboard overlay.
        """
        # Create a copy to draw the overlay
        overlay = frame.copy()
        
        # Draw each key
        for key, (x, y, w, h) in self.key_rectangles.items():
            # Determine key color based on state
            if key == self.current_hover_key:
                color = self.key_hover_color
            else:
                color = self.key_color
            
            # Draw key rectangle with rounded corners effect
            cv2.rectangle(overlay, (x, y), (x + w, y + h), color, -1)
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), 2)
            
            # Draw key text
            text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            text_x = x + (w - text_size[0]) // 2
            text_y = y + (h + text_size[1]) // 2
            cv2.putText(overlay, key, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.text_color, 2)
        
        # Blend overlay with original frame for transparency
        cv2.addWeighted(overlay, self.keyboard_alpha, frame, 1 - self.keyboard_alpha, 0, frame)
        
        return frame
    
    def check_hover(self, cursor_x, cursor_y):
        """
        Check if cursor is hovering over any key and handle hover timing.
        
        Args:
            cursor_x (int): X coordinate of cursor in frame.
            cursor_y (int): Y coordinate of cursor in frame.
        
        Returns:
            tuple: (hovered_key, hover_progress) or (None, 0) if not hovering.
        """
        current_time = time.time()
        hovered_key = None
        
        # Check which key the cursor is over
        for key, (x, y, w, h) in self.key_rectangles.items():
            if x <= cursor_x <= x + w and y <= cursor_y <= y + h:
                hovered_key = key
                break
        
        # Update hover state
        if hovered_key:
            if hovered_key != self.current_hover_key:
                # Started hovering over a new key
                self.current_hover_key = hovered_key
                self.hover_start_time = current_time
            else:
                # Continue hovering over same key
                hover_duration = current_time - self.hover_start_time
                
                # Check if hover threshold reached
                if hover_duration >= self.hover_threshold:
                    # Check cooldown to prevent repeated typing
                    if current_time - self.last_typed_time > self.typing_cooldown:
                        self.type_key(hovered_key)
                        self.last_typed_key = hovered_key
                        self.last_typed_time = current_time
                        # Reset hover to prevent continuous typing
                        self.hover_start_time = current_time
                
                # Calculate progress (0.0 to 1.0)
                progress = min(hover_duration / self.hover_threshold, 1.0)
                return hovered_key, progress
        else:
            # Not hovering over any key
            self.current_hover_key = None
            self.hover_start_time = None
        
        return hovered_key, 0.0
    
    def handle_click(self, cursor_x, cursor_y):
        """
        Handle a click gesture on the keyboard.
        
        Args:
            cursor_x (int): X coordinate of cursor in frame.
            cursor_y (int): Y coordinate of cursor in frame.
        
        Returns:
            str or None: The key that was clicked, or None if no key was clicked.
        """
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_typed_time < self.typing_cooldown:
            return None
        
        # Check which key was clicked
        for key, (x, y, w, h) in self.key_rectangles.items():
            if x <= cursor_x <= x + w and y <= cursor_y <= y + h:
                self.type_key(key)
                self.last_typed_key = key
                self.last_typed_time = current_time
                return key
        
        return None
    
    def type_key(self, key):
        """
        Type the specified key using pyautogui.
        
        Args:
            key (str): The key to type.
        """
        try:
            if key == 'SPACE':
                pyautogui.press('space')
                print(f"✓ Typed: [SPACE]")
            elif key == 'ENTER':
                pyautogui.press('enter')
                print(f"✓ Typed: [ENTER]")
            elif key == 'BACK':
                pyautogui.press('backspace')
                print(f"✓ Typed: [BACKSPACE]")
            else:
                # Regular character
                pyautogui.press(key.lower())
                print(f"✓ Typed: {key}")
        except Exception as e:
            print(f"✗ Error typing key '{key}': {e}")
    
    def draw_hover_indicator(self, frame, key, progress):
        """
        Draw a visual indicator showing hover progress on a key.
        
        Args:
            frame (numpy.ndarray): The video frame to draw on.
            key (str): The key being hovered over.
            progress (float): Hover progress from 0.0 to 1.0.
        
        Returns:
            numpy.ndarray: Frame with hover indicator.
        """
        if key not in self.key_rectangles:
            return frame
        
        x, y, w, h = self.key_rectangles[key]
        
        # Draw progress bar above the key
        bar_height = 8
        bar_y = y - bar_height - 5
        bar_width = int(w * progress)
        
        # Background bar
        cv2.rectangle(frame, (x, bar_y), (x + w, bar_y + bar_height), (100, 100, 100), -1)
        
        # Progress bar
        color = (0, int(255 * progress), int(255 * (1 - progress)))  # Green to red gradient
        cv2.rectangle(frame, (x, bar_y), (x + bar_width, bar_y + bar_height), color, -1)
        
        # Progress text
        progress_text = f"{int(progress * 100)}%"
        cv2.putText(frame, progress_text, (x + 5, bar_y - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def toggle_visibility(self):
        """
        Toggle keyboard visibility (could be used for showing/hiding keyboard).
        """
        self.keyboard_alpha = 0.6 if self.keyboard_alpha == 0 else 0
    
    def get_typed_text_display(self, frame):
        """
        Display the last typed key on the frame.
        
        Args:
            frame (numpy.ndarray): The video frame to draw on.
        
        Returns:
            numpy.ndarray: Frame with typed text display.
        """
        if self.last_typed_key and (time.time() - self.last_typed_time < 2.0):
            # Show last typed key for 2 seconds
            text = f"Typed: {self.last_typed_key}"
            cv2.putText(frame, text, (10, self.keyboard_y_offset - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return frame
