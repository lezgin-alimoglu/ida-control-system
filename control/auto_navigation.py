from pymavlink import mavutil
import config

def set_mode(master, mode_str):
    """
    Change ArduPilot mode (e.g.: 'GUIDED', 'AUTO', 'MANUAL')
    """
    try:
        mode_id = master.mode_mapping()[mode_str.upper()]
        master.set_mode(mode_id)
        print(f"[INFO] Flight mode {mode_str.upper()} set.")
    except Exception as e:
        print(f"[ERROR] Mode değiştirilemedi: {e}")

def send_goto_location(master, lat, lon, alt=5.0):
    """
    Sends a global position target (goto command) to the vehicle in GUIDED mode.
    Latitude and Longitude should be in decimal degrees.
    Altitude is in meters (relative to home).
    """
    master.mav.set_position_target_global_int_send(
        0,  # time_boot_ms (not used)
        config.TARGET_SYSTEM,
        config.TARGET_COMPONENT,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b110111111000,  # Only position enabled
        int(lat * 1e7),  # Latitude in 1e7 format
        int(lon * 1e7),  # Longitude in 1e7 format
        alt,             # Altitude in meters (relative)
        0, 0, 0,         # Velocity (not used)
        0, 0, 0,         # Acceleration (not used)
        0, 0             # Yaw, yaw rate (not used)
    )
    print(f"[INFO] Goto command sent to ({lat}, {lon}, {alt}m)")

def clear_mission(master):
    """
    Clears all mission items from the vehicle.
    """
    master.mav.mission_clear_all_send(
        config.TARGET_SYSTEM,
        config.TARGET_COMPONENT
    )
    print("[INFO] Existing mission cleared.")

def upload_mission(master, waypoints):
    """
    Uploads a list of waypoints to the vehicle.
    Each waypoint is a tuple: (lat, lon, alt)
    """
    try:
        # Enter mission upload mode
        master.waypoint_clear_all_send()
        master.waypoint_count_send(len(waypoints))

        for i, (lat, lon, alt) in enumerate(waypoints):
            master.mav.mission_item_send(
                config.TARGET_SYSTEM,
                config.TARGET_COMPONENT,
                i,                                # Sequence
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                0, 1,                             # current, autocontinue
                0, 0, 0, 0,                       # param1-4: hold time, acceptance radius, etc.
                lat, lon, alt                     # lat, lon, alt
            )
            print(f"[INFO] Waypoint {i} sent: ({lat}, {lon}, {alt})")

        print("[✓] Mission upload complete.")
    except Exception as e:
        print(f"[ERROR] Görev yüklenemedi: {e}")

def start_mission(master):
    """
    Switches to AUTO mode and starts mission from first waypoint.
    """
    try:
        set_mode(master, "AUTO")

        master.mav.command_long_send(
            config.TARGET_SYSTEM,
            config.TARGET_COMPONENT,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,
            0,   # first item index
            0,   # last item index (0 = all)
            0, 0, 0, 0, 0
        )

        print("[✓] Mission started in AUTO mode.")
    except Exception as e:
        print(f"[ERROR] Görev başlatılamadı: {e}")
