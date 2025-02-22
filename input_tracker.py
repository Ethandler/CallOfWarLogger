import keyboard
import mouse
from threading import Lock
import logging
import os
import sys

class InputTracker:
    def __init__(self):
        self.lock = Lock()
        self.current_keys = set()
        self.mouse_position = (0, 0)
        self.mouse_buttons = set()
        self.is_tracking = False
        self.input_tracking_available = True

    def _check_privileges(self):
        """Check if we have necessary privileges for input tracking."""
        if sys.platform.startswith('linux'):
            try:
                keyboard.on_press(lambda _: None)
                keyboard.unhook_all()
                return True
            except ImportError as e:
                if "You must be root" in str(e):
                    logging.warning("Input tracking requires root privileges on Linux. Running with limited functionality.")
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

            # Set up mouse hooks
            mouse.on_move(self._on_mouse_move)
            mouse.on_click(self._on_mouse_click)
            mouse.on_scroll(self._on_mouse_scroll)

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
                mouse.unhook_all()
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

    def _on_mouse_move(self, x, y):
        """Handle mouse movement events."""
        with self.lock:
            self.mouse_position = (x, y)

    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        with self.lock:
            if pressed:
                self.mouse_buttons.add(button)
            else:
                self.mouse_buttons.discard(button)

    def _on_mouse_scroll(self, x, y, dx, dy):
        """Handle mouse scroll events."""
        pass  # Implement if scroll tracking is needed

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
            return {
                "keyboard": list(self.current_keys),
                "mouse_position": self.mouse_position,
                "mouse_buttons": list(self.mouse_buttons),
                "tracking_enabled": True
            }