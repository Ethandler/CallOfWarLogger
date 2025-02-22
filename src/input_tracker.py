"""Module for tracking keyboard and mouse inputs."""
from pynput import keyboard, mouse
from datetime import datetime
import threading
import time
from typing import Dict, Set, Tuple
import math

class InputTracker:
    def __init__(self):
        self.active_keys: Set[str] = set()
        self.mouse_position: Tuple[int, int] = (0, 0)
        self.mouse_pressed: Dict[str, bool] = {'left': False, 'right': False}
        self.last_mouse_movement = datetime.now()
        
        # Initialize listeners
        self.keyboard_listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.mouse_listener = mouse.Listener(
            on_move=self._on_mouse_move,
            on_click=self._on_mouse_click
        )
        
    def start(self):
        """Start tracking inputs."""
        self.keyboard_listener.start()
        self.mouse_listener.start()
        
    def stop(self):
        """Stop tracking inputs."""
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        
    def _on_key_press(self, key):
        """Handle key press events."""
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        self.active_keys.add(key_char)
        
    def _on_key_release(self, key):
        """Handle key release events."""
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)
        self.active_keys.discard(key_char)
        
    def _on_mouse_move(self, x, y):
        """Handle mouse movement events."""
        self.mouse_position = (x, y)
        self.last_mouse_movement = datetime.now()
        
    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events."""
        if button == mouse.Button.left:
            self.mouse_pressed['left'] = pressed
        elif button == mouse.Button.right:
            self.mouse_pressed['right'] = pressed
            
    def get_current_state(self) -> Dict:
        """Get the current state of all inputs."""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_keys': list(self.active_keys),
            'mouse_position': self.mouse_position,
            'mouse_buttons': self.mouse_pressed,
            'time_since_last_movement': (datetime.now() - self.last_mouse_movement).total_seconds()
        }
        
    def calculate_aim_metrics(self) -> Dict:
        """Calculate aiming-related metrics."""
        center_x, center_y = 1920/2, 1080/2  # Assuming 1080p resolution
        mouse_x, mouse_y = self.mouse_position
        
        # Calculate distance from center
        distance = math.sqrt((mouse_x - center_x)**2 + (mouse_y - center_y)**2)
        
        # Calculate angle
        angle = math.atan2(mouse_y - center_y, mouse_x - center_x)
        
        return {
            'distance_from_center': distance,
            'angle': math.degrees(angle),
            'is_ads': self.mouse_pressed['right']
        }
