import folium
from folium.plugins import MousePosition
import webbrowser
import os

def create_map(center_lat=40.0, center_lon=29.0, zoom=17):
    """
    Creates an interactive map with coordinate display.
    Returns the full path to the saved HTML file.
    """
    try:
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

        MousePosition().add_to(m)

        map_file = "mission_map.html"
        m.save(map_file)

        abs_path = os.path.abspath(map_file)
        try:
            webbrowser.open(f"file://{abs_path}")

            print("[✓] Map opened in browser.")
        except Exception as e:
            print(f"[ERROR] Map could not be opened in browser: {e}")

        print("[→] Click on the map and manually record coordinates from the bottom-right.")

        return abs_path
    except Exception as e:
        print(f"[ERROR] Map could not be created: {e}")
        return None
