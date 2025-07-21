'''This script sends fake GPS data to GUI'''
import socket
import time

GUI_IP = "127.0.0.1"  # Aynı makinedeyse localhost
GUI_PORT = 5005       # GUI'nin dinlediği port (GPS_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Örnek konumlar (çember çizer gibi)
lat, lon = 39.9010, 32.7550

print("[SET_GPS] GPS verisi gönderilmeye başlandı...")

try:
    while True:
        msg = f"GPS:{lat:.6f},{lon:.6f}"
        sock.sendto(msg.encode(), (GUI_IP, GUI_PORT))
        print(f"[SET_GPS] Gönderildi → {msg}")

        lat += 0.00005
        lon += 0.00005

        time.sleep(1)
except KeyboardInterrupt:
    print("\n[SET_GPS] Durduruldu.")
