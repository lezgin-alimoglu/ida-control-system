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
        print(f"[ERROR] Mode could not be changed: {e}")

def send_goto_location(master, lat, lon, alt=5.0):
    """
    Sends a global position target (goto command) to the vehicle in GUIDED mode.
    """
    master.mav.set_position_target_global_int_send(
        0,  # time_boot_ms
        config.TARGET_SYSTEM,
        config.TARGET_COMPONENT,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b110111111000,  # Position only
        int(lat * 1e7),
        int(lon * 1e7),
        alt,
        0, 0, 0,   # vx, vy, vz
        0, 0, 0,   # ax, ay, az
        0, 0       # yaw, yaw_rate
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
        clear_mission(master)

        master.mav.mission_count_send(
            config.TARGET_SYSTEM,
            len(waypoints)
        )

        for i, (lat, lon, alt) in enumerate(waypoints):
            master.mav.mission_item_send(
                config.TARGET_SYSTEM,
                config.TARGET_COMPONENT,
                i,  # seq
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                2 if i == 0 else 0,  # current
                1,  # autocontinue
                0,    # hold time (sec)
                0,    # acceptance radius
                0,    # pass radius
                0,    # yaw angle
                lat, lon, alt
            )
            print(f"[INFO] Waypoint {i} uploaded: ({lat}, {lon}, {alt})")

        print("[✓] Mission upload complete.")
    except Exception as e:
        print(f"[ERROR] Mission could not be uploaded: {e}")

def start_mission(master):
    """
    Switches to AUTO mode and starts mission from first waypoint.
    """
    try:
        set_mode(master, "AUTO")
        time.sleep(1)

        master.mav.command_long_send(
            config.TARGET_SYSTEM,
            config.TARGET_COMPONENT,
            mavutil.mavlink.MAV_CMD_MISSION_START,
            0,
            0,  # first waypoint index
            0,  # last waypoint index (0 = all)
            0, 0, 0, 0, 0
        )
        print("[✓] Mission started in AUTO mode.")
    except Exception as e:
        print(f"[ERROR] Mission could not be started: {e}")
