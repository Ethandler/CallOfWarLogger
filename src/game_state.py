"""Module for tracking and estimating game state."""
from datetime import datetime
from typing import Dict, Optional
import math

class GameState:
    def __init__(self):
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.rotation = {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0}
        self.health = 100
        self.armor = 0
        self.current_weapon = "primary"
        self.ammo = {'current': 30, 'reserve': 90}
        self.game_time = 0.0
        self.last_update = datetime.now()
        self.is_in_combat = False
        self.last_damage_time = None
        self.score = 0
        self.kills = 0
        self.deaths = 0
        
    def update(self, input_state: Dict) -> None:
        """Update game state based on input state."""
        current_time = datetime.now()
        delta_time = (current_time - self.last_update).total_seconds()
        
        # Update position based on movement keys
        self._update_position(input_state, delta_time)
        
        # Update rotation based on mouse movement
        self._update_rotation(input_state)
        
        # Update combat state
        self._update_combat_state(input_state)
        
        self.game_time += delta_time
        self.last_update = current_time
        
    def _update_position(self, input_state: Dict, delta_time: float) -> None:
        """Update player position based on input state."""
        speed = 4.8  # Base movement speed in meters per second
        
        # Apply sprint multiplier if sprinting
        if 'shift' in input_state['active_keys']:
            speed *= 1.5
            
        # Calculate movement vector
        movement_x = movement_z = 0.0
        if 'w' in input_state['active_keys']: movement_z += 1
        if 's' in input_state['active_keys']: movement_z -= 1
        if 'd' in input_state['active_keys']: movement_x += 1
        if 'a' in input_state['active_keys']: movement_x -= 1
        
        # Normalize and apply movement
        if movement_x != 0 or movement_z != 0:
            magnitude = math.sqrt(movement_x**2 + movement_z**2)
            movement_x = movement_x / magnitude * speed * delta_time
            movement_z = movement_z / magnitude * speed * delta_time
            
            # Apply movement relative to current rotation
            yaw_rad = math.radians(self.rotation['yaw'])
            final_x = movement_x * math.cos(yaw_rad) - movement_z * math.sin(yaw_rad)
            final_z = movement_x * math.sin(yaw_rad) + movement_z * math.cos(yaw_rad)
            
            self.position['x'] += final_x
            self.position['z'] += final_z
            
    def _update_rotation(self, input_state: Dict) -> None:
        """Update player rotation based on mouse movement."""
        mouse_x, mouse_y = input_state['mouse_position']
        center_x, center_y = 1920/2, 1080/2  # Assuming 1080p resolution
        
        # Calculate rotation changes
        self.rotation['yaw'] += (mouse_x - center_x) * 0.1
        self.rotation['pitch'] = max(-89, min(89, self.rotation['pitch'] + (mouse_y - center_y) * 0.1))
        
    def _update_combat_state(self, input_state: Dict) -> None:
        """Update combat-related state information."""
        # Check for shooting
        if input_state['mouse_buttons']['left']:
            if self.ammo['current'] > 0:
                self.ammo['current'] -= 1
                
        # Check for reloading
        if 'r' in input_state['active_keys'] and self.ammo['current'] < 30:
            self._reload()
            
    def _reload(self) -> None:
        """Handle weapon reloading."""
        if self.ammo['reserve'] > 0:
            needed = 30 - self.ammo['current']
            taken = min(needed, self.ammo['reserve'])
            self.ammo['current'] += taken
            self.ammo['reserve'] -= taken
            
    def get_state(self) -> Dict:
        """Get current game state."""
        return {
            'timestamp': datetime.now().isoformat(),
            'position': self.position,
            'rotation': self.rotation,
            'health': self.health,
            'armor': self.armor,
            'current_weapon': self.current_weapon,
            'ammo': self.ammo,
            'game_time': self.game_time,
            'is_in_combat': self.is_in_combat,
            'score': self.score,
            'kills': self.kills,
            'deaths': self.deaths
        }
