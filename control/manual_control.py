import pygame
from pymavlink import mavutil
import config

def init_joystick():
    """
    Initializes the joystick and returns the first joystick. Returns None if no joystick is found.
    """
    try:
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            print("[ERROR] Joystick not found! Please connect a joystick and try again.")
            return None

        js = pygame.joystick.Joystick(0)
        js.init()
        print(f"[✓] Joystick connected: {js.get_name()}")
        return js
    except Exception as e:
        print(f"[ERROR] Joystick could not be initialized: {e}")
        return None

def constrain(val, min_val, max_val):
    """
    Constrains a value to the given minimum and maximum range.
    """
    return max(min(val, max_val), min_val)


def run_manual(master):
    """
    Starts the manual control loop with joystick.
    """
    js = init_joystick()
    if js is None:
        print("[INFO] Manual control could not be started. Returning to main menu.")
        return
    
    print("[INFO] Manual control started. To exit, press Ctrl+C")

    try:
        while True:
            pygame.event.pump()  # Update joystick

            thrust = -js.get_axis(1)  # Left stick Y → forward/backward (up -1)
            steer = js.get_axis(0)    # Left stick X → right/left (right +1)

            # Catamaran motor calculation
            ch1_pwm = int(1500 + (thrust + steer) * 400)
            ch2_pwm = int(1500 + (thrust - steer) * 400)

            master.mav.rc_channels_override_send(
                config.TARGET_SYSTEM,
                config.TARGET_COMPONENT,
                ch1_pwm, ch2_pwm,
                1500, 1500, 1500, 1500, 1500, 1500
            )
    except KeyboardInterrupt:
        print("\n[INFO] Manual control stopped.")
    except Exception as e:
        print(f"[ERROR] Error during manual control: {e}")
