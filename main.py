import time
from pymavlink import mavutil
import config
from control.manual_control import run_manual  # Manual kontrol fonksiyonu
from control.autonomous_navigation import (              # Otonom görev fonksiyonları
    set_mode,
    clear_mission,
    upload_mission,
    start_mission
)

def connect_vehicle():
    print("[INFO] Connecting to vehicle...")
    master = mavutil.mavlink_connection(
        config.MAVLINK_CONNECTION_STRING,
        baud=config.MAVLINK_BAUDRATE
    )
    master.wait_heartbeat()
    print(f"[✓] Connected to system {master.target_system}, component {master.target_component}")
    return master

def run_autonomous(master):
    print("[INFO] Switching to GUIDED mode...")
    set_mode(master, "GUIDED")

    # 📍 Örnek waypoint listesi — bunları gerçek koordinatlarla değiştir
    waypoints = [
        (39.909736, 32.807465, 5.0),
        (39.909850, 32.807600, 5.0),
        (39.909950, 32.807465, 5.0)
    ]

    print("[INFO] Uploading mission...")
    clear_mission(master)
    upload_mission(master, waypoints)

    print("[INFO] Starting mission...")
    start_mission(master)

def main():
    while True:
        print("\n=== IDA CONTROL SYSTEM ===")
        print("1 - Manual Control (Joystick)")
        print("2 - Autonomous Mission")
        print("0 - Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            master = connect_vehicle()
            run_manual(master)
        elif choice == "2":
            master = connect_vehicle()
            run_autonomous(master)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
