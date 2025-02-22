import keyboard
import logging
import os
import sys
from threading import Lock

class InputTracker:
    def __init__(self):
        self.lock = Lock()
        self.current_keys = set()
        self.mouse_position = (0, 0)
        self.mouse_buttons = set()
        self.is_tracking = False
        self.input_tracking_available = True
        self.mouse = None

        # Try to import pynput, but don't fail if it's not available
        try:
            from pynput.mouse import Controller as MouseController
            self.mouse = MouseController()
            logging.info("Mouse controller initialized successfully")
        except Exception as e:
            logging.warning(f"Mouse tracking unavailable: {str(e)}")
            self.mouse = None

    def _check_privileges(self):
        """Check if we have necessary privileges for input tracking."""
        if sys.platform.startswith('linux'):
            try:
                keyboard.on_press(lambda _: None)
                keyboard.unhook_all()
                return True
            except Exception as e:
                logging.warning(f"Input tracking requires root privileges on Linux: {str(e)}")
                self.input_tracking_available = False
                return False
        return True

    def start(self):
        """Start tracking keyboard and mouse inputs if available."""
        self.is_tracking = True

        if not self._check_privileges():
            logging.warning("Input tracking is disabled. Game state will still be logged.")
            return

        try:
            # Set up keyboard hooks
            keyboard.on_press(self._on_key_press)
            keyboard.on_release(self._on_key_release)
            logging.info("Keyboard tracking initialized successfully")

            if self.mouse:
                self.mouse_position = self.mouse.position
                logging.info("Mouse tracking initialized successfully")
            else:
                logging.warning("Mouse tracking unavailable")

            logging.info("Input tracking started successfully")
        except Exception as e:
            logging.error(f"Failed to initialize input tracking: {str(e)}")
            self.input_tracking_available = False

    def stop(self):
        """Stop tracking inputs."""
        self.is_tracking = False
        if self.input_tracking_available:
            try:
                keyboard.unhook_all()
                logging.info("Input tracking stopped")
            except Exception as e:
                logging.error(f"Error while stopping input tracking: {str(e)}")

    def _on_key_press(self, event):
        """Handle key press events."""
        with self.lock:
            self.current_keys.add(event.name)

    def _on_key_release(self, event):
        """Handle key release events."""
        with self.lock:
            self.current_keys.discard(event.name)

    def get_current_input_state(self):
        """Return the current state of all inputs."""
        if not self.input_tracking_available:
            return {
                "keyboard": [],
                "mouse_position": (0, 0),
                "mouse_buttons": [],
                "tracking_enabled": False
            }

        with self.lock:
            try:
                if self.mouse:
                    self.mouse_position = self.mouse.position
            except Exception as e:
                logging.error(f"Failed to get mouse position: {str(e)}")

            return {
                "keyboard": list(self.current_keys),
                "mouse_position": self.mouse_position,
                "mouse_buttons": list(self.mouse_buttons),
                "tracking_enabled": True
            }