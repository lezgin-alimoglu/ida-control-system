from pymavlink import mavutil 
import config
def connect_mavlink():
    try:
        print(f"[INFO] Starting connection: {config.MAVLINK_CONNECTION_STRING} @ {config.MAVLINK_BAUDRATE} baud")
        # MAVLink connection
        master = mavutil.mavlink_connection(
            config.MAVLINK_CONNECTION_STRING,
            baud=config.MAVLINK_BAUDRATE
        )
        # Wait for heartbeat
        print("[INFO] Waiting for heartbeat...")
        master.wait_heartbeat()
        print(f"[✓] Connected: system={master.target_system}, component={master.target_component}")
        # MAVLink version optional
        try:
            print(f"[INFO] MAVLink version: {master.get_mavlink_version()}")
        except AttributeError:
            print("[INFO] MAVLink version information could not be retrieved.")
        return master
    except Exception as e:
        print(f"[ERROR] MAVLink connection failed: {e}")
        return None

