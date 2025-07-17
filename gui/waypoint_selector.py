import folium
from folium.plugins import MousePosition
import webbrowser
import os

waypoints = []

def on_click(event):
    lat, lon = event['latlng']
    waypoints.append((lat, lon, 10.0))  # Varsayılan yükseklik 10m
    print(f"[WAYPOINT] {lat:.6f}, {lon:.6f}, 10.0")

def create_map(center_lat=40.0, center_lon=29.0, zoom=17, save_file="waypoints.txt"):
    """
    Creates an interactive map with coordinate display and waypoint saving.
    Returns the full path to the saved HTML file.
    """
    try:
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
        MousePosition().add_to(m)

        # Add click listener via JavaScript
        m.add_child(folium.LatLngPopup())

        map_file = "mission_map.html"
        m.save(map_file)

        abs_path = os.path.abspath(map_file)
        try:
            webbrowser.open(f"file://{abs_path}")
            print("[✓] Map opened in browser.")
        except Exception as e:
            print(f"[ERROR] Map could not be opened in browser: {e}")

        print("[→] Click on the map. After selecting all waypoints, close the browser tab.")
        input("Press Enter here after you have finished selecting waypoints and closed the map...")

        # Read waypoints from mission_map.html (LatLngPopup shows them in browser, user must copy them)
        print("Paste the coordinates you copied from the map, one per line (lat, lon, alt). Type 'done' to finish:")
        user_waypoints = []
        while True:
            line = input()
            if line.strip().lower() == 'done':
                break
            try:
                parts = [float(x) for x in line.strip().split(",")]
                if len(parts) == 2:
                    parts.append(10.0)  # Varsayılan yükseklik
                user_waypoints.append(tuple(parts))
            except Exception:
                print("Invalid format. Please enter as: lat, lon [, alt]")
        if user_waypoints:
            with open(save_file, "w") as f:
                for wp in user_waypoints:
                    f.write(f"{wp[0]},{wp[1]},{wp[2]}\n")
            print(f"[✓] Waypoints saved to {save_file}")
        else:
            print("[!] No waypoints entered.")
        return abs_path
    except Exception as e:
        print(f"[ERROR] Map could not be created: {e}")
        return None
