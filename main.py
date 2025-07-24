import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

'''Main CLI controller for switching modes'''
import os
import subprocess
import time
import sys
from comm.jetson_comm import send_command_pwm
from control.manual_mode import run_manual

def stop_motors():
    print("[MAIN] Boats are stopping...")
    # Jetson'a UDP mesajı gönder: m1_1500, m3_1500
    import comm.jetson_comm as jc
    jc.send_command_pwm(1, 1500)
    jc.send_command_pwm(2, 1500)
    print("[MAIN] Tüm motorlar nötr PWM'de.")

def run_gui():
    print("[MAIN] GUI starting.")
    subprocess.Popen(["python3", "gui/base_station_gui.py"])

def run_auto_mode():
    print("[MAIN] Auto mode is started")
    subprocess.call(["python3", "control/auto_nav.py"])

def run_manual_mode():
    print("[MAIN] Manuel mod is started.")
    run_manual()

def return_to_launch():
    print("[MAIN] RTL command send.")
    with open("mission.txt") as f:
        first = f.readline().strip()
        with open("rtl_target.txt", "w") as out:
            out.write(first)
    subprocess.call(["python3", "control/rtl_mode.py"])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use in such format: python3 main.py [auto|manual|rtl]")
        sys.exit(1)

    mode = sys.argv[1].lower()

    run_gui()  

    try:
        if mode == "auto":
            run_auto_mode()
        elif mode == "manual":
            run_manual_mode()
        elif mode == "rtl":
            return_to_launch()
        else:
            print("Error: Wrong Type")
    except KeyboardInterrupt:
        print("\n[MAIN] Exit by CTRL+C .")
    finally:
        stop_motors()
