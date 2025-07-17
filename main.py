import time
from pymavlink import mavutil
import config
from control.manual_control import run_manual  # manual_control.py içinde fonksiyon

def connect_vehicle():
    print("[INFO] Connecting to vehicle...")
    master = mavutil.mavlink_connection(
        config.CONNECTION_STRING,
        baud=config.BAUD_RATE
    )
    master.wait_heartbeat()
    print(f"[✓] Connected to system {master.target_system}, component {master.target_component}")
    return master

def main():
    while True:
        print("\n=== IDA CONTROL SYSTEM ===")
        print("1 - Manual Control (Joystick)")
        print("0 - Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            master = connect_vehicle()
            run_manual(master)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
