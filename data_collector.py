import time
import logging
from utils import performance_monitor

class DataCollector:
    def __init__(self):
        self.last_game_state = None
        self.last_update = time.time()
        self.last_action = None
        self.behavior_start_time = time.time()
        self.current_behavior = "neutral"  # Can be: aggressive, defensive, neutral

    @performance_monitor
    def get_game_state(self):
        """
        Collect current game state data.
        This is a mock implementation - in real usage, this would interface
        with the game's memory or API.
        """
        current_time = time.time()

        # Track time spent in current behavior
        behavior_duration = current_time - self.behavior_start_time

        # Mock game state data for CoD: World at War Zombies
        game_state = {
            "player": {
                "position": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "camera": {
                    "pitch": 0.0,
                    "yaw": 0.0,
                    "roll": 0.0
                },
                "health": 100,
                "armor": 100,
                "weapon": {
                    "active": "primary",
                    "ammo": {
                        "current": 30,
                        "reserve": 120
                    },
                    "name": "MP40",
                    "last_reload_time": current_time,
                    "shots_fired": 0,
                    "hits": 0,
                    "accuracy": 0.0
                },
                "perks": {
                    "juggernog": False,
                    "quick_revive": False,
                    "double_tap": False,
                    "speed_cola": False
                },
                "points": 500,
                "behavior": {
                    "current": self.current_behavior,
                    "duration": behavior_duration
                }
            },
            "game": {
                "time_elapsed": current_time - self.last_update,
                "round": 1,
                "zombies": {
                    "total": 24,
                    "alive": 20,
                    "spawned": 4,
                    "killed": 0
                },
                "power_ups": {
                    "active": None,  # Can be: "insta_kill", "double_points", "max_ammo", "nuke"
                    "time_remaining": 0
                },
                "score": 0,
                "outcomes": {
                    "kills": 0,
                    "headshots": 0,
                    "damage_dealt": 0,
                    "deaths": 0,
                    "revives": 0
                }
            },
            "environment": {
                "enemies_visible": [],
                "in_cover": False,
                "doors_open": [],
                "power_on": False,
                "interactive_objects": {
                    "mystery_box_location": "spawn",
                    "active_traps": [],
                    "available_doors": [
                        {"id": "door_1", "cost": 750},
                        {"id": "door_2", "cost": 1000}
                    ]
                }
            },
            "actions": {
                "last_action": self.last_action,
                "tactical": {
                    "peeking": False,
                    "sprinting": False,
                    "crouching": False
                }
            }
        }

        self.last_game_state = game_state
        self.last_update = current_time

        return game_state

    def update_game_state(self, new_state):
        """Update the current game state with new data."""
        self.last_game_state = new_state
        self.last_update = time.time()

    def update_behavior(self, new_behavior):
        """Update player behavior tracking."""
        if new_behavior != self.current_behavior:
            self.current_behavior = new_behavior
            self.behavior_start_time = time.time()

    def record_action(self, action_type, details):
        """Record a player action with timestamp."""
        self.last_action = {
            "type": action_type,
            "details": details,
            "timestamp": time.time()
        }