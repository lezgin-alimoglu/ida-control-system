import sys
import os
import time
import json
from math import radians, degrees, atan2, sin, cos
from comm.jetson_comm import send_command_pwm
from config import KP, KI, KD, PWM_MIN, PWM_MAX

# === PID Controller Class ===
class PID:
    def __init__(self, kp, ki, kd, setpoint=0, out_min=None, out_max=None):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.setpoint = setpoint
        self._prev_error = 0
        self._integral = 0
        self.out_min = out_min
        self.out_max = out_max

    def update(self, measurement, dt):
        error = (self.setpoint - measurement + 540) % 360 - 180  # Normalize between -180 and 180
        self._integral += error * dt
        derivative = (error - self._prev_error) / dt if dt > 0 else 0
        output = self.kp * error + self.ki * self._integral + self.kd * derivative
        self._prev_error = error

        # Clamp output
        if self.out_min is not None:
            output = max(self.out_min, output)
        if self.out_max is not None:
            output = min(self.out_max, output)
        return output

# === Calculate Bearing Between Two GPS Points ===
def calculate_bearing(lat1, lon1, lat2, lon2):
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    x = sin(dLon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)

    initial_bearing = atan2(x, y)
    return (degrees(initial_bearing) + 360) % 360

# === Read Current Position from File ===
def read_position():
    try:
        position_file = os.path.join(os.path.dirname(__file__), "..", "position.json")
        with open(position_file, "r") as f:
            pos = json.load(f)
            return pos["lat"], pos["lon"], pos["yaw"]
    except Exception as e:
        print(f"[AUTO] Position read error: {e}")
        return None

# === Load Waypoints from Mission File ===
def load_mission():
    mission = []
    mission_file = os.path.join(os.path.dirname(__file__), "..", "mission.txt")
    with open(mission_file, "r") as f:
        for line in f:
            lat, lon = map(float, line.strip().split(","))
            mission.append((lat, lon))
    return mission

# === Check if Target Reached Based on Proximity ===
def reached(lat1, lon1, lat2, lon2, threshold=0.0001):
    return abs(lat1 - lat2) < threshold and abs(lon1 - lon2) < threshold

# === Clamp PWM Values Safely ===
def clamp_pwm(value):
    return max(PWM_MIN, min(PWM_MAX, value))

# === Main Auto Navigation Logic ===
def run_auto_mode():
    print("[AUTO] Mission started.")
    mission = load_mission()
    if not mission:
        print("[AUTO] No waypoints found.")
        return

    yaw_pid = PID(KP, KI, KD, out_min=-400, out_max=400)
    base_pwm = 1500
    prev_time = time.time()

    for idx, (target_lat, target_lon) in enumerate(mission):
        print(f"[AUTO] Navigating to Waypoint {idx+1}: ({target_lat:.6f}, {target_lon:.6f})")

        while True:
            now = time.time()
            dt = now - prev_time
            prev_time = now

            pos = read_position()
            if pos is None:
                print("[AUTO] Waiting for position...")
                time.sleep(1)
                continue

            lat, lon, yaw = pos

            if reached(lat, lon, target_lat, target_lon):
                print(f"[AUTO] Waypoint {idx+1} reached.")
                break

            target_bearing = calculate_bearing(lat, lon, target_lat, target_lon)
            yaw_pid.setpoint = target_bearing
            correction = yaw_pid.update(yaw, dt)

            pwm_left = clamp_pwm(int(base_pwm - correction))
            pwm_right = clamp_pwm(int(base_pwm + correction))

            send_command_pwm(1, pwm_left)
            send_command_pwm(2, pwm_right)

            print(f"[AUTO] Target: {target_bearing:.1f}° | Yaw: {yaw:.1f}° | Correction: {correction:.1f} → PWM L:{pwm_left}, R:{pwm_right}")
            time.sleep(0.25)

    send_command_pwm(1, 1500)
    send_command_pwm(2, 1500)
    print("[AUTO] Mission completed. Motors stopped.")

# === Entry Point ===
if __name__ == "__main__":
    try:
        run_auto_mode()
    except KeyboardInterrupt:
        print("[AUTO] Interrupted by user. Stopping motors.")
        send_command_pwm(1, 1500)
        send_command_pwm(2, 1500)
