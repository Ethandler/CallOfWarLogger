import keyboard
import logging
import os
import sys
from threading import Lock
import mouse
import ctypes

class InputTracker:
    def __init__(self):
        self.lock = Lock()
        self.current_keys = set()
        self.mouse_position = (0, 0)
        self.mouse_buttons = set()
        self.is_tracking = False
        self.input_tracking_available = True
        self._check_privileges()

    def _check_privileges(self):
        """Check if we have necessary privileges for input tracking."""
        try:
            if sys.platform.startswith('win32'):
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if not is_admin:
                    logging.warning("Input tracking requires administrator privileges on Windows")
                    self.input_tracking_available = False
                    return False
                logging.info("Running with administrator privileges")
                return True
            elif sys.platform.startswith('linux'):
                try:
                    keyboard.on_press(lambda _: None)
                    keyboard.unhook_all()
                    return True
                except Exception as e:
                    logging.warning(f"Input tracking requires root privileges on Linux: {str(e)}")
                    self.input_tracking_available = False
                    return False
            return True
        except Exception as e:
            logging.error(f"Error checking privileges: {str(e)}")
            self.input_tracking_available = False
            return False

    def start(self):
        """Start tracking keyboard and mouse inputs if available."""
        if not self.input_tracking_available:
            logging.warning("Input tracking is disabled. Game state will still be logged.")
            return

        try:
            # Set up keyboard hooks
            keyboard.on_press(self._on_key_press)
            keyboard.on_release(self._on_key_release)
            logging.info("Keyboard tracking initialized successfully")

            # Set up mouse hooks
            mouse.on_click(self._on_mouse_click)
            mouse.on_move(self._on_mouse_move)
            logging.info("Mouse tracking initialized successfully")

            self.is_tracking = True
            logging.info("Input tracking started successfully")

        except Exception as e:
            logging.error(f"Failed to initialize input tracking: {str(e)}")
            self.input_tracking_available = False

    def stop(self):
        """Stop tracking inputs."""
        if self.is_tracking:
            try:
                keyboard.unhook_all()
                mouse.unhook_all()
                self.is_tracking = False
                logging.info("Input tracking stopped successfully")
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

    def _on_mouse_click(self, event):
        """Handle mouse click events."""
        with self.lock:
            if hasattr(event, 'button'):
                self.mouse_buttons.add(event.button)

    def _on_mouse_move(self, event):
        """Handle mouse movement events."""
        with self.lock:
            if hasattr(event, 'x') and hasattr(event, 'y'):
                self.mouse_position = (event.x, event.y)

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
                # Get current mouse position even if tracking is disabled
                try:
                    current_pos = mouse.get_position()
                    self.mouse_position = current_pos
                except Exception as e:
                    logging.error(f"Failed to get mouse position: {str(e)}")

                return {
                    "keyboard": list(self.current_keys),
                    "mouse_position": self.mouse_position,
                    "mouse_buttons": list(self.mouse_buttons),
                    "tracking_enabled": True
                }
            except Exception as e:
                logging.error(f"Error getting input state: {str(e)}")
                return {
                    "keyboard": [],
                    "mouse_position": (0, 0),
                    "mouse_buttons": [],
                    "tracking_enabled": False
                }