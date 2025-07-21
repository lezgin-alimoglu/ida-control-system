# test/test_comm.py

import sys
import os
import time

# Üst dizini sys.path'e ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from comm.jetson_comm import send_command_pwm

print("Jetson'a PWM komutu gönderme testi başlatılıyor...")

# Test komutları
send_command_pwm(1, 1500)
time.sleep(1)

send_command_pwm(1, 1700)
time.sleep(1)

send_command_pwm(1, 1500)
time.sleep(1)


send_command_pwm(2, 1500)
time.sleep(1)


send_command_pwm(2, 1700)
time.sleep(1)


send_command_pwm(2, 1500)
time.sleep(1)
print("Tüm komutlar gönderildi.")
