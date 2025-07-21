import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import pygame
import time
from comm.jetson_comm import send_command_pwm  

def init_joystick(): # Logitech F710
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("[ERROR] Joystick not found!")
        return None
    js = pygame.joystick.Joystick(0)
    js.init()
    print(f"[✓] Joystick connected: {js.get_name()}")
    return js


def constrain(val, min_val, max_val):
    return max(min_val, min(max_val, val))

def run_manual():
    js = init_joystick()
    if js is None:
        return

    print("[INFO] Manual mode started. Press Ctrl+C to stop.")

    try:
        while True:
            pygame.event.pump()

            thrust = -js.get_axis(1)  
            steer = js.get_axis(0)   

            # PWM values are between 1100 and 1900
            left_pwm = int(1500 + constrain(thrust + steer, -1, 1) * 400)
            right_pwm = int(1500 + constrain(thrust - steer, -1, 1) * 400)

            send_command_pwm(1, left_pwm+8)
            send_command_pwm(2, right_pwm+8)

            print(f"[MANUAL] PWM → L: {left_pwm}, R: {right_pwm}")
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[INFO] Manual mode stopped.")
        # Durdurmak için PWM’leri merkeze çek
        send_command_pwm(1, 1500)
        send_command_pwm(2, 1500)
        print("[INFO] Motors neutralized (1500µs)")
