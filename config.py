# Configuration settings for the game logger

# Logging settings
LOG_SETTINGS = {
    "frequency": 60,  # Logging frequency in Hz
    "batch_size": 1000,  # Number of entries before auto-save
    "format": "json"  # Log format (json or csv)
}

# Input tracking settings
INPUT_SETTINGS = {
    "track_keyboard": True,
    "track_mouse": True,
    "track_mouse_position": True,
    "track_mouse_buttons": True
}

# Performance monitoring settings
PERFORMANCE_SETTINGS = {
    "monitor_cpu": True,
    "monitor_memory": True,
    "warning_threshold_cpu": 80,  # Percentage
    "warning_threshold_memory": 80  # Percentage
}

# File settings
FILE_SETTINGS = {
    "log_directory": "game_logs",
    "max_file_size_mb": 100,
    "compression": False
}
