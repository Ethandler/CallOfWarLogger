"""Configuration settings for the game data logging system."""

# Input tracking settings
MOUSE_POLLING_RATE = 60  # Hz
KEYBOARD_TRACKING_ENABLED = True
MOUSE_TRACKING_ENABLED = True

# Logging settings
LOG_FILE_PATH = "game_logs.json"
LOGGING_INTERVAL = 0.1  # seconds

# Game state estimation
PLAYER_SPEED = 4.8  # meters per second (walking speed)
SPRINT_MULTIPLIER = 1.5

# Performance monitoring
PERFORMANCE_LOG_INTERVAL = 5  # seconds
MAX_CPU_USAGE = 80  # percentage
MAX_MEMORY_USAGE = 500  # MB

# Key bindings (default CoD:WaW)
KEYBINDS = {
    'forward': 'w',
    'backward': 's',
    'left': 'a',
    'right': 'd',
    'jump': 'space',
    'crouch': 'ctrl_l',
    'sprint': 'shift',
    'reload': 'r',
    'primary_weapon': '1',
    'secondary_weapon': '2',
    'interact': 'f'
}
