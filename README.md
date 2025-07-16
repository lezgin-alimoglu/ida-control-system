# IDA Control System

## Description
This project includes a ground control station and automatic/manual control systems for an unmanned surface vehicle (IDA). It communicates via the MAVLink protocol, supports manual control with a joystick, and offers mission planning (waypoint) features.

## Setup

1. **Python 3.7+** must be installed.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. For joystick support on Linux, you may need extra packages:
   ```bash
   sudo apt-get install joystick python3-tk
   ```

## Usage

```bash
python main.py
```

- **1 - Manual Control:** Control the vehicle manually with a joystick.
- **2 - Mission Planner (GUI):** Enter waypoint coordinates and send the vehicle on an autonomous mission.
- **0 - Exit:** Exit the program.

## Dependencies
- pymavlink
- pygame
- folium
- pyserial
- tkinter (comes with most Python installations, but may require python3-tk on some Linux distros)

## Hardware Requirements
- MAVLink-compatible vehicle (e.g., ArduPilot-based)
- Connection via USB or UDP
- Joystick (for manual control)

## Important Notes
- Adjust MAVLink connection settings in the `config.py` file as needed.
- Some parts of the code are hardware-dependent and may not work on all platforms.
- For bugs or suggestions, please open an issue.
