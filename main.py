import time
from pymavlink import mavutil
import config
from control.manual_control import run_manual  # manual_control.py içinde fonksiyon
from control.auto_navigation import upload_mission, start_mission
from gui.waypoint_selector import create_map

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.button import Button

class WaypointSelector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.mapview = MapView(zoom=17, lat=40.0, lon=29.0)
        self.add_widget(self.mapview)
        self.waypoints = []

        self.save_btn = Button(text="Kaydet ve Kapat", size_hint_y=None, height=50)
        self.save_btn.bind(on_release=self.save_and_close)
        self.add_widget(self.save_btn)

        self.mapview.bind(on_touch_down=self.on_map_touch)

    def on_map_touch(self, instance, touch):
        if self.mapview.collide_point(*touch.pos) and touch.button == 'left':
            lat, lon = self.mapview.get_latlon_at(*touch.pos)
            # Marker zaten varsa sil, yoksa ekle
            for marker in self.mapview.children[:]:
                if isinstance(marker, MapMarker) and abs(marker.lat - lat) < 0.0001 and abs(marker.lon - lon) < 0.0001:
                    self.mapview.remove_widget(marker)
                    self.waypoints = [wp for wp in self.waypoints if not (abs(wp[0] - lat) < 0.0001 and abs(wp[1] - lon) < 0.0001)]
                    return
            marker = MapMarker(lat=lat, lon=lon)
            self.mapview.add_widget(marker)
            self.waypoints.append((lat, lon, 10.0))
        return False

    def save_and_close(self, *args):
        with open("waypoints.txt", "w") as f:
            for wp in self.waypoints:
                f.write(f"{wp[0]},{wp[1]},{wp[2]}\n")
        App.get_running_app().stop()

class WaypointApp(App):
    def build(self):
        return WaypointSelector()

def connect_vehicle():
    print("[INFO] Connecting to vehicle...")
    master = mavutil.mavlink_connection(
        config.MAVLINK_CONNECTION_STRING,
        baud=config.MAVLINK_BAUDRATE
    )
    master.wait_heartbeat()
    print(f"[✓] Connected to system {master.target_system}, component {master.target_component}")
    return master

def read_waypoints_from_file(filename="waypoints.txt"):
    waypoints = []
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = [float(x) for x in line.strip().split(",")]
                if len(parts) == 3:
                    waypoints.append(tuple(parts))
        print(f"[INFO] {len(waypoints)} waypoints loaded from {filename}")
    except Exception as e:
        print(f"[ERROR] Could not read waypoints: {e}")
    return waypoints

def main():
    while True:
        print("\n=== IDA CONTROL SYSTEM ===")
        print("1 - Manual Control (Joystick)")
        print("2 - Select Waypoints on Map and Start Mission")
        print("0 - Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            master = connect_vehicle()
            run_manual(master)
        elif choice == "2":
            WaypointApp().run() # Kullanıcıdan waypoint dosyasını oluşturmasını iste
            waypoints = read_waypoints_from_file()
            if not waypoints:
                print("[!] No waypoints found. Please select waypoints on the map first.")
                continue
            master = connect_vehicle()
            upload_mission(master, waypoints)
            start_mission(master)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
