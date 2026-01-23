"""
Voice Control Module
Handles voice commands using speech recognition in a separate thread.
Supports commands for opening applications, typing text, and keyboard actions.
"""

import speech_recognition as sr
import pyautogui
import subprocess
import threading
import time
import os


class VoiceController:
    """
    A class to handle voice commands using speech recognition.
    Runs in a separate thread to avoid blocking the main application.
    """

    def __init__(self, callback=None):
        """
        Initialize the VoiceController.
        
        Args:
            callback (function): Optional callback function to report status/commands.
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.thread = None
        self.callback = callback
        self.stop_flag = threading.Event()
        
        # Configure recognizer for better performance
        self.recognizer.energy_threshold = 4000  # Adjust based on ambient noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Seconds of silence to consider end of phrase
        
        # Command mapping
        self.app_commands = {
            'chrome': ['chrome', 'google chrome', 'browser'],
            'notepad': ['notepad', 'text editor'],
            'calculator': ['calculator', 'calc'],
            'explorer': ['explorer', 'file explorer', 'files'],
            'cmd': ['command prompt', 'cmd', 'terminal'],
            'paint': ['paint', 'mspaint'],
        }
        
        # Keyboard commands
        self.keyboard_commands = {
            'enter': ['enter', 'return'],
            'escape': ['escape', 'cancel'],
            'backspace': ['backspace', 'delete', 'back space'],
            'space': ['space', 'spacebar'],
            'tab': ['tab'],
        }
        
        print("✓ Voice controller initialized")
        print("  Calibrating microphone... (Please wait)")
        self._calibrate_microphone()

    def _calibrate_microphone(self):
        """
        Calibrate the microphone for ambient noise.
        """
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✓ Microphone calibrated")
        except Exception as e:
            print(f"⚠ Warning: Could not calibrate microphone: {e}")

    def start_listening(self):
        """
        Start listening for voice commands in a separate thread.
        """
        if not self.is_listening:
            self.is_listening = True
            self.stop_flag.clear()
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print("🎤 Voice control started (listening in background)")
            return True
        return False

    def stop_listening(self):
        """
        Stop listening for voice commands.
        """
        if self.is_listening:
            self.is_listening = False
            self.stop_flag.set()
            if self.thread:
                self.thread.join(timeout=2)
            print("🎤 Voice control stopped")
            return True
        return False

    def _listen_loop(self):
        """
        Main listening loop that runs in a separate thread.
        Continuously listens for voice commands.
        """
        while self.is_listening and not self.stop_flag.is_set():
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                try:
                    # Recognize speech using Google Speech Recognition
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"🎤 Heard: '{command}'")
                    
                    # Report to callback if provided
                    if self.callback:
                        self.callback(f"Heard: {command}")
                    
                    # Process the command
                    self._process_command(command)
                    
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    print(f"⚠ Speech recognition service error: {e}")
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                pass
            except Exception as e:
                print(f"⚠ Voice control error: {e}")
                time.sleep(0.5)

    def _process_command(self, command):
        """
        Process a recognized voice command.
        
        Args:
            command (str): The recognized command text.
        """
        command = command.lower().strip()
        
        # Check for "open" commands
        if command.startswith('open '):
            app_name = command.replace('open ', '').strip()
            self._open_application(app_name)
            return
        
        # Check for "type" commands
        if command.startswith('type '):
            text = command.replace('type ', '').strip()
            self._type_text(text)
            return
        
        # Check for keyboard commands
        for key, phrases in self.keyboard_commands.items():
            if any(phrase in command for phrase in phrases):
                self._press_key(key)
                return
        
        # Check for special commands
        if 'stop listening' in command or 'stop voice' in command:
            print("✓ Voice: Stopping voice control")
            self.stop_listening()
            return
        
        if 'show keyboard' in command or 'open keyboard' in command:
            print("✓ Voice: Command to show keyboard")
            if self.callback:
                self.callback("SHOW_KEYBOARD")
            return
        
        if 'hide keyboard' in command or 'close keyboard' in command:
            print("✓ Voice: Command to hide keyboard")
            if self.callback:
                self.callback("HIDE_KEYBOARD")
            return
        
        # If no command matched
        print(f"⚠ Voice: Unknown command '{command}'")

    def _open_application(self, app_name):
        """
        Open an application based on voice command.
        
        Args:
            app_name (str): The application name to open.
        """
        # Find matching application
        for app, keywords in self.app_commands.items():
            if any(keyword in app_name for keyword in keywords):
                try:
                    if os.name == 'nt':  # Windows
                        if app == 'chrome':
                            subprocess.Popen(['start', 'chrome'], shell=True)
                        elif app == 'notepad':
                            subprocess.Popen(['notepad.exe'])
                        elif app == 'calculator':
                            subprocess.Popen(['calc.exe'])
                        elif app == 'explorer':
                            subprocess.Popen(['explorer.exe'])
                        elif app == 'cmd':
                            subprocess.Popen(['cmd.exe'])
                        elif app == 'paint':
                            subprocess.Popen(['mspaint.exe'])
                    else:  # Linux/Mac
                        subprocess.Popen([app])
                    
                    print(f"✓ Voice: Opening {app}")
                    if self.callback:
                        self.callback(f"Opening {app}")
                    return
                except Exception as e:
                    print(f"✗ Voice: Error opening {app}: {e}")
                    return
        
        print(f"⚠ Voice: Application '{app_name}' not recognized")

    def _type_text(self, text):
        """
        Type text using pyautogui.
        
        Args:
            text (str): The text to type.
        """
        try:
            # Small delay to allow user to focus on target window
            time.sleep(0.2)
            pyautogui.typewrite(text, interval=0.05)
            print(f"✓ Voice: Typed '{text}'")
            if self.callback:
                self.callback(f"Typed: {text}")
        except Exception as e:
            print(f"✗ Voice: Error typing text: {e}")

    def _press_key(self, key):
        """
        Press a keyboard key.
        
        Args:
            key (str): The key name to press.
        """
        try:
            pyautogui.press(key)
            print(f"✓ Voice: Pressed '{key}'")
            if self.callback:
                self.callback(f"Pressed: {key}")
        except Exception as e:
            print(f"✗ Voice: Error pressing key: {e}")

    def is_active(self):
        """
        Check if voice control is currently active.
        
        Returns:
            bool: True if listening, False otherwise.
        """
        return self.is_listening

    def test_microphone(self):
        """
        Test if the microphone is working.
        
        Returns:
            bool: True if microphone is accessible, False otherwise.
        """
        try:
            with self.microphone as source:
                print("🎤 Testing microphone... Say something!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio)
                print(f"✓ Microphone test successful! Heard: '{text}'")
                return True
        except sr.WaitTimeoutError:
            print("⚠ Microphone test: No speech detected")
            return False
        except Exception as e:
            print(f"✗ Microphone test failed: {e}")
            return False


# Example usage
if __name__ == "__main__":
    def status_callback(message):
        print(f"[Callback] {message}")
    
    # Create voice controller
    voice = VoiceController(callback=status_callback)
    
    # Test microphone
    voice.test_microphone()
    
    # Start listening
    voice.start_listening()
    
    print("\nVoice commands:")
    print("  - 'Open Chrome' / 'Open Notepad' / 'Open Calculator'")
    print("  - 'Type [your text]'")
    print("  - 'Enter' / 'Backspace' / 'Escape'")
    print("  - 'Show Keyboard' / 'Hide Keyboard'")
    print("  - 'Stop Listening'")
    print("\nPress Ctrl+C to exit")
    
    try:
        while voice.is_active():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
        voice.stop_listening()
