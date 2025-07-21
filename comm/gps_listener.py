import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

'''This script for listening GPS'''
import socket
import json
import config
import os

GPS_PORT = config.GPS_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", GPS_PORT))  


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
position_file = os.path.join(BASE_DIR, "position.json")


print(f"[GPS Listener] Started on port {GPS_PORT}. Saving to {position_file}")


while True:
    data, _ = sock.recvfrom(1024)
    try:
        msg = data.decode().strip()
        print(msg)
        if msg.startswith("GPS:"):
            payload = msg.replace("GPS:", "")
            lat_str, lon_str, yaw_str, speed_str = payload.split(",")
            
            lat = float(lat_str)
            lon = float(lon_str)
            yaw = float(yaw_str.replace("Yaw:", "").replace("°", ""))
            speed = float(speed_str.replace("Speed:", "").replace("m/s", ""))

            with open(position_file, "w") as f:
                json.dump({
                    "lat": lat,
                    "lon": lon,
                    "yaw": yaw,
                    "speed": speed
                }, f)
    except Exception as e:
        print("[GPS Listener] Error:", e)
