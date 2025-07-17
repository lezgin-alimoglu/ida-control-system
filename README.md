# IDA Control System

## Description
This project includes a ground control station and automatic/manual control systems for an unmanned surface vehicle (IDA). It communicates via the MAVLink protocol, supports manual control with a joystick, and offers mission planning (waypoint) features.

## Setup

1. **Python 3.7+** must be installed.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. For joystick support on Linux, you may need extra packages:
   ```bash
   sudo apt-get install joystick python3-tk
   ```

## Usage

```bash
python main.py
```

- **1 - Manual Control:** Control the vehicle manually with a joystick.
- **2 - Mission Planner (GUI):** Enter waypoint coordinates and send the vehicle on an autonomous mission.
- **0 - Exit:** Exit the program.

## Dependencies
- pymavlink
- pygame
- folium
- pyserial
- tkinter (comes with most Python installations, but may require python3-tk on some Linux distros)

## Hardware Requirements
- MAVLink-compatible vehicle (e.g., ArduPilot-based)
- Connection via USB or UDP
- Joystick (for manual control)

## Important Notes
- Adjust MAVLink connection settings in the `config.py` file as needed.
- Some parts of the code are hardware-dependent and may not work on all platforms.
- For bugs or suggestions, please open an issue.

# IDA Control System - Görev Başlatma Akışı

## Harita Üzerinden Waypoint Seçip Görev Başlatma

1. **Programı başlatın:**
   ```bash
   python3 main.py
   ```

2. **Menüden 'Select Waypoints on Map and Start Mission' seçeneğini (2) seçin.**

3. **Açılan haritada istediğiniz noktalara tıklayın.**
   - Her tıklamada koordinatlar ekranda görünecek.
   - Tüm noktaları seçtikten sonra harita sekmesini kapatın.

4. **Terminalde 'Press Enter here...' mesajı geldiğinde Enter'a basın.**

5. **Terminalde, haritada tıkladığınız noktaların koordinatlarını (lat, lon, alt) sırayla girin.**
   - Örnek: `40.123456,29.123456,10.0`
   - Sadece lat,lon girerseniz yükseklik otomatik 10.0 alınır.
   - Tüm noktaları girdikten sonra `done` yazıp Enter'a basın.

6. **Program, waypoint'leri kaydedecek ve Ardupilot'a yükleyecek. Görev otomatik başlatılır.**

---

- Waypoint dosyası: `waypoints.txt`
- Görev yükleme ve başlatma işlemleri otomatik yapılır.
- Hatalar veya eksik girişlerde terminalde uyarı alırsınız.
