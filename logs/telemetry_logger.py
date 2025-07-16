import csv
import time
import os
from pymavlink import mavutil

def start_logging(master, log_dir="logs", filename_prefix="telemetry"):
    """
    Starts a background telemetry logger.
    Records GPS, velocity, heading, and RC override data to CSV.
    """
    try:
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        filename = f"{filename_prefix}_{int(time.time())}.csv"
        filepath = os.path.join(log_dir, filename)
        print(f"[INFO] Logging started → {filepath}")
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                "timestamp",
                "lat", "lon", "alt",
                "vx", "vy", "vz",
                "heading",
                "rc1", "rc2", "rc3", "rc4"
            ])
            # Değişkenleri başta None olarak tanımla
            lat = lon = alt = vx = vy = vz = heading = None
            rc = [None, None, None, None]
            try:
                while True:
                    msg = master.recv_match(blocking=True)
                    now = time.time()
                    if msg.get_type() == "GLOBAL_POSITION_INT":
                        lat = msg.lat / 1e7
                        lon = msg.lon / 1e7
                        alt = msg.alt / 1e3
                        heading = msg.hdg / 100.0 if msg.hdg != 65535 else None
                    elif msg.get_type() == "VFR_HUD":
                        vx = msg.groundspeed
                        vz = msg.climb
                    elif msg.get_type() == "RC_CHANNELS":
                        rc = [msg.chan1_raw, msg.chan2_raw, msg.chan3_raw, msg.chan4_raw]
                        # Tüm gerekli değişkenler tanımlıysa yaz
                        if None not in [lat, lon, alt, vx, vz, heading]:
                            writer.writerow([
                                now,
                                lat, lon, alt,
                                vx, 0, vz,
                                heading,
                                *rc
                            ])
                            csvfile.flush()
            except KeyboardInterrupt:
                print("\n[INFO] Telemetry logging stopped.")
            except Exception as e:
                print(f"[ERROR] Telemetri kaydı sırasında hata: {e}")
    except Exception as e:
        print(f"[ERROR] Telemetri kaydı başlatılamadı: {e}")

