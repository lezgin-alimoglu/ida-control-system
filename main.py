import time
from pymavlink import mavutil
import config
from control.manual_control import run_manual  # manual_control.py içinde fonksiyon
from control.auto_navigation import upload_mission, start_mission
from gui.waypoint_selector import create_map

def connect_vehicle():
    print("[INFO] Connecting to vehicle...")
    master = mavutil.mavlink_connection(
        config.MAVLINK_CONNECTION_STRING,
        baud=config.MAVLINK_BAUDRATE
    )
    master.wait_heartbeat()
    print(f"[✓] Connected to system {master.target_system}, component {master.target_component}")
    return master

def read_waypoints_from_file(filename="waypoints.txt"):
    waypoints = []
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = [float(x) for x in line.strip().split(",")]
                if len(parts) == 3:
                    waypoints.append(tuple(parts))
        print(f"[INFO] {len(waypoints)} waypoints loaded from {filename}")
    except Exception as e:
        print(f"[ERROR] Could not read waypoints: {e}")
    return waypoints

def main():
    while True:
        print("\n=== IDA CONTROL SYSTEM ===")
        print("1 - Manual Control (Joystick)")
        print("2 - Select Waypoints on Map and Start Mission")
        print("0 - Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            master = connect_vehicle()
            run_manual(master)
        elif choice == "2":
            create_map()  # Kullanıcıdan waypoint dosyasını oluşturmasını iste
            waypoints = read_waypoints_from_file()
            if not waypoints:
                print("[!] No waypoints found. Please select waypoints on the map first.")
                continue
            master = connect_vehicle()
            upload_mission(master, waypoints)
            start_mission(master)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
