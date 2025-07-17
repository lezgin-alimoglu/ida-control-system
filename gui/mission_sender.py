from pymavlink import mavutil
import config
import time

def send_mission(waypoints):
    """
    Uploads a list of (lat, lon) waypoints to the vehicle using MAVLink mission protocol.
    """
    print(f"[INFO] Connecting to vehicle on {config.CONNECTION_STRING}...")
    master = mavutil.mavlink_connection(config.CONNECTION_STRING, baud=config.BAUDRATE)
    master.wait_heartbeat()
    print(f"[✓] Connected. System ID: {master.target_system}, Component ID: {master.target_component}")

    # Clear existing missions
    print("[INFO] Clearing existing mission items...")
    master.mav.mission_clear_all_send(master.target_system, master.target_component)
    time.sleep(1)

    # Create mission items
    print(f"[INFO] Sending {len(waypoints)} mission items...")
    for i, (lat, lon) in enumerate(waypoints):
        master.mav.mission_item_int_send(
            master.target_system,
            master.target_component,
            i,  # seq
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 1,  # current, autocontinue
            0, 0, 0, 0,  # params 1–4
            int(lat * 1e7),
            int(lon * 1e7),
            2.0  # altitude
        )
        time.sleep(0.1)

    # Send mission count
    master.mav.mission_count_send(master.target_system, master.target_component, len(waypoints))
    print("[✓] Mission uploaded.")

    # Wait for ACK
    while True:
        msg = master.recv_match(type=['MISSION_ACK', 'MISSION_REQUEST'], blocking=True)
        if msg.get_type() == 'MISSION_ACK':
            print(f"[✓] Mission acknowledged with result: {msg.type}")
            break
        elif msg.get_type() == 'MISSION_REQUEST':
            print(f"[INFO] Requested mission item: {msg.seq}")
        else:
            print(f"[WARNING] Unknown message: {msg}")
