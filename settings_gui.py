"""
Settings GUI Module
A tkinter-based settings window for adjusting virtual mouse parameters in real-time.
"""

import tkinter as tk
from tkinter import ttk
import threading


class SettingsGUI:
    """
    A class to create and manage the settings GUI window for the virtual mouse.
    This runs in a separate thread alongside the OpenCV loop.
    """

    def __init__(self):
        """
        Initialize the Settings GUI with default values.
        """
        # Shared variables that will be updated by sliders
        self.smoothing_factor = 7  # Default smoothing factor
        self.mouse_sensitivity = 150  # Default padding (frame reduction margin)
        
        # Flag to track if GUI is running
        self.is_running = False
        
        # Thread reference
        self.gui_thread = None
        
        # Window reference
        self.root = None

    def create_gui(self):
        """
        Create the tkinter GUI window with sliders.
        This method runs in a separate thread.
        """
        self.root = tk.Tk()
        self.root.title("Virtual Mouse Settings")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set window to stay on top
        self.root.attributes('-topmost', True)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title label
        title_label = ttk.Label(main_frame, text="Virtual Mouse Settings", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # ==================== SMOOTHING FACTOR SLIDER ====================
        # Label for smoothing factor
        smoothing_label = ttk.Label(main_frame, text="Smoothing Factor (Jitter Control)", 
                                    font=('Arial', 10, 'bold'))
        smoothing_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Description
        smoothing_desc = ttk.Label(main_frame, 
                                   text="Higher = Smoother but slower cursor movement",
                                   font=('Arial', 8), foreground='gray')
        smoothing_desc.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Smoothing factor slider (1-20)
        self.smoothing_scale = tk.Scale(
            main_frame,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            length=300,
            command=self.update_smoothing,
            tickinterval=5,
            resolution=1
        )
        self.smoothing_scale.set(self.smoothing_factor)
        self.smoothing_scale.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Current value label for smoothing
        self.smoothing_value_label = ttk.Label(main_frame, 
                                               text=f"Current: {self.smoothing_factor}",
                                               font=('Arial', 9))
        self.smoothing_value_label.grid(row=4, column=0, columnspan=2, pady=(0, 20))
        
        # ==================== MOUSE SENSITIVITY SLIDER ====================
        # Label for sensitivity
        sensitivity_label = ttk.Label(main_frame, text="Mouse Sensitivity (Frame Margin)", 
                                      font=('Arial', 10, 'bold'))
        sensitivity_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Description
        sensitivity_desc = ttk.Label(main_frame, 
                                     text="Lower = Easier to reach screen edges, Higher = More precise control",
                                     font=('Arial', 8), foreground='gray')
        sensitivity_desc.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Sensitivity slider (50-300)
        self.sensitivity_scale = tk.Scale(
            main_frame,
            from_=50,
            to=300,
            orient=tk.HORIZONTAL,
            length=300,
            command=self.update_sensitivity,
            tickinterval=50,
            resolution=10
        )
        self.sensitivity_scale.set(self.mouse_sensitivity)
        self.sensitivity_scale.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        # Current value label for sensitivity
        self.sensitivity_value_label = ttk.Label(main_frame, 
                                                 text=f"Current: {self.mouse_sensitivity}px",
                                                 font=('Arial', 9))
        self.sensitivity_value_label.grid(row=8, column=0, columnspan=2, pady=(0, 10))
        
        # ==================== RESET BUTTON ====================
        reset_button = ttk.Button(main_frame, text="Reset to Defaults", 
                                  command=self.reset_defaults)
        reset_button.grid(row=9, column=0, columnspan=2, pady=(10, 0))
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.is_running = True
        self.root.mainloop()

    def update_smoothing(self, value):
        """
        Callback function when smoothing slider is moved.
        
        Args:
            value (str): The new slider value as a string.
        """
        self.smoothing_factor = int(float(value))
        self.smoothing_value_label.config(text=f"Current: {self.smoothing_factor}")
        print(f"[Settings] Smoothing factor updated to: {self.smoothing_factor}")

    def update_sensitivity(self, value):
        """
        Callback function when sensitivity slider is moved.
        
        Args:
            value (str): The new slider value as a string.
        """
        self.mouse_sensitivity = int(float(value))
        self.sensitivity_value_label.config(text=f"Current: {self.mouse_sensitivity}px")
        print(f"[Settings] Mouse sensitivity (padding) updated to: {self.mouse_sensitivity}px")

    def reset_defaults(self):
        """
        Reset all settings to their default values.
        """
        # Reset smoothing factor
        self.smoothing_factor = 7
        self.smoothing_scale.set(7)
        self.smoothing_value_label.config(text=f"Current: {self.smoothing_factor}")
        
        # Reset sensitivity
        self.mouse_sensitivity = 150
        self.sensitivity_scale.set(150)
        self.sensitivity_value_label.config(text=f"Current: {self.mouse_sensitivity}px")
        
        print("[Settings] All settings reset to defaults")

    def on_closing(self):
        """
        Handle the window close event.
        """
        print("[Settings] Settings window closed")
        self.is_running = False
        if self.root:
            self.root.quit()
            self.root.destroy()

    def start(self):
        """
        Start the settings GUI in a separate thread.
        """
        if not self.is_running:
            self.gui_thread = threading.Thread(target=self.create_gui, daemon=True)
            self.gui_thread.start()
            print("[Settings] Settings GUI started in separate thread")

    def stop(self):
        """
        Stop the settings GUI.
        """
        if self.is_running and self.root:
            self.is_running = False
            self.root.quit()
            print("[Settings] Settings GUI stopped")

    def get_smoothing_factor(self):
        """
        Get the current smoothing factor value.
        
        Returns:
            int: The current smoothing factor.
        """
        return self.smoothing_factor

    def get_mouse_sensitivity(self):
        """
        Get the current mouse sensitivity (padding) value.
        
        Returns:
            int: The current mouse sensitivity in pixels.
        """
        return self.mouse_sensitivity


# For testing the GUI standalone
if __name__ == "__main__":
    print("Starting Settings GUI test...")
    settings = SettingsGUI()
    settings.start()
    
    # Keep the main thread alive
    try:
        while settings.is_running:
            import time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        settings.stop()
