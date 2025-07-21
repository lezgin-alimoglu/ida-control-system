# test/test_auto.py
import sys
import os

# control klasörünü import yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from control.auto_nav import calculate_bearing, yaw_to_pwm

# Test konumları
current_lat, current_lon = 39.9000, 32.7500
target_lat, target_lon = 39.9010, 32.7520
yaw_current = 70.0  # varsayılan yönümüz
base_pwm = 1600

# Bearing hesapla
yaw_target = calculate_bearing(current_lat, current_lon, target_lat, target_lon)

# PWM hesapla
left_pwm, right_pwm = yaw_to_pwm(yaw_current, yaw_target, base_pwm)

# Sonuçları yazdır
print(f"[TEST] Target Bearing: {yaw_target:.2f}°")
print(f"[TEST] Yaw Current: {yaw_current:.2f}°")
print(f"[TEST] PWM Output → Left: {left_pwm}, Right: {right_pwm}")
