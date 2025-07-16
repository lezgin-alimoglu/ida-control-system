from comms.mavlink_interface import connect_mavlink
from control.manual_control import run_manual
from gui.ground_station_ui import launch_gui

def main():
    """
    IDA Control System ana menü fonksiyonu. Kullanıcıdan mod seçimi alır ve ilgili kontrol modunu başlatır.
    """
    master = connect_mavlink()
    if master is None:
        print("[ERROR] MAVLink bağlantısı kurulamadı. Program sonlandırılıyor.")
        return
    while True:
        print("\n====== IDA CONTROL SYSTEM ======")
        print("1 - Manual Control (Joystick)")
        print("2 - Mission Planner (GUI)")
        print("0 - Exit")
        try:
            choice = input("Select mode: ")
        except Exception as e:
            print(f"[ERROR] Girdi alınamadı: {e}")
            continue
        if choice == "1":
            run_manual(master)
        elif choice == "2":
            launch_gui(master)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
