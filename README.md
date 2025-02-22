# Game Data Logger for Call of Duty: World at War

A Python-based game data logging system designed for capturing comprehensive player interactions in Call of Duty: World at War, with a focus on flexible input tracking and performance-efficient data collection.

## Features

- Real-time game state logging (position, health, ammo, etc.)
- Input tracking (keyboard and mouse)
- Performance monitoring
- JSON-based data storage
- Cross-platform support (with privileged access requirements on Linux)

## Requirements

- Python 3.11+
- Root/Administrator privileges (for input tracking)
- Required packages: `keyboard`, `mouse`, `psutil`
- Call of Duty: World at War (Steam version)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ChanNEthanOS/COD-Logger.git
cd COD-Logger
```

2. Install dependencies:
```bash
pip install keyboard mouse psutil
```

## Usage

### Running with Full Functionality (Including Input Tracking)

#### On Windows 10:
Method 1 (Recommended):
1. Double-click `run_logger.bat`
2. If prompted, click "Yes" to allow administrator access

Method 2 (Manual):
1. Right-click on Command Prompt or PowerShell
2. Select "Run as Administrator"
3. Navigate to the project directory
4. Run the script:
```bash
python game_logger.py
```

## Data Collection

The logger captures:

1. Game State Data:
   - Player position (X, Y, Z coordinates)
   - Camera angle (pitch, yaw, roll)
   - Health and armor
   - Ammo count
   - Active weapon
   - Enemy positions
   - Cover detection
   - Game time elapsed
   - Objective progress

2. Player Actions (when run with privileges):
   - Movement inputs (WASD, crouch, jump, sprint)
   - Aiming (mouse movement)
   - Shooting and reloading
   - Weapon switching
   - Tactical decisions (peeking, rotating, flanking)
   - Interaction with objects (doors, vehicles)
   - Time spent in different behaviors (aggressive, defensive)

3. Outcome Data:
   - Hit or Miss tracking
   - Kill/Damage tracking
   - Death event logging
   - Score and point system
   - Perk and power-up status

## Zombies Mode Specific Features

- Round tracking
- Perk system monitoring (Juggernog, Speed Cola, etc.)
- Power status tracking
- Door state management
- Mystery Box location
- Zombie count and status
- Points system
- Power-up tracking

## Output Format

Data is stored in JSON format with timestamps:
```json
{
    "timestamp": 1645577291.456,
    "game_state": {
        "player": {
            "position": {"x": 0, "y": 0, "z": 0},
            "camera": {"pitch": 0, "yaw": 0, "roll": 0},
            "health": 100,
            "armor": 100,
            "weapon": {"active": "primary", "ammo": {"current": 30, "reserve": 120}}
        },
        "game": {
            "round": 1,
            "zombies": {"total": 24, "alive": 20},
            "power_ups": {"active": null}
        }
    },
    "input_data": {
        "keyboard": ["w", "shift"],
        "mouse_position": [500, 300],
        "mouse_buttons": ["left"],
        "tracking_enabled": true
    }
}
```

## License

MIT License - See LICENSE file for details