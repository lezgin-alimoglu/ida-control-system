# logger.py
import csv
import os
import time

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "mission_log.csv")

def init_logger():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "lat", "lon", "yaw", 
                "target_bearing", "yaw_error", "correction", 
                "pwm_left", "pwm_right"
            ])

def log_data(lat, lon, yaw, target_bearing, yaw_error, correction, pwm_left, pwm_right):
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            round(time.time(), 2), lat, lon, yaw,
            round(target_bearing, 2), round(yaw_error, 2), round(correction, 2),
            pwm_left, pwm_right
        ])
