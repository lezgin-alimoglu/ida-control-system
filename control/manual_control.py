import pygame
from pymavlink import mavutil
import config

def init_joystick():
    """
    Joystick'i başlatır ve ilk joystick'i döndürür. Joystick yoksa None döner.
    """
    try:
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            print("[ERROR] Joystick bulunamadı! Lütfen bir joystick bağlayın ve tekrar deneyin.")
            return None
        js = pygame.joystick.Joystick(0)
        js.init()
        print(f"[✓] Joystick connected: {js.get_name()}")
        return js
    except Exception as e:
        print(f"[ERROR] Joystick başlatılamadı: {e}")
        return None

def constrain(val, min_val, max_val):
    """
    Bir değeri verilen minimum ve maksimum aralığa sınırlar.
    """
    return max(min(val, max_val), min_val)


def run_manual(master):
    """
    Joystick ile manuel kontrol döngüsünü başlatır.
    """
    js = init_joystick()
    if js is None:
        print("[INFO] Manuel kontrol başlatılamadı. Ana menüye dönülüyor.")
        return
    print("[INFO] Manual control started. To exit, press Ctrl+C")
    try:
        while True:
            pygame.event.pump()  # Update joystick
            thrust = -js.get_axis(1)  # Left stick Y → forward/backward (up -1)
            steer = js.get_axis(0)    # Left stick X → right/left (right +1)
            # Katamaran motor hesabı
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
        print(f"[ERROR] Manuel kontrol sırasında hata: {e}")
