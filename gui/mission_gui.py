import folium
from folium.plugins import MousePosition
import webbrowser
import os
import config
from kivy_garden.mapview import MapView, MapMarker

waypoints = []  # (lat, lon)

# Create HTML map
def generate_map():
    m = folium.Map(location=[39.92, 32.85], zoom_start=15)

    MousePosition().add_to(m)

    m.add_child(folium.LatLngPopup())  # ↩️ Tıklanan yeri popup'ta gösterir

    # Save
    map_file = 'waypoint_map.html'
    m.save(map_file)
    print(f"[✓] Map saved as {map_file}. Click on map to get coordinates.")
    webbrowser.open('file://' + os.path.realpath(map_file))


# Manually add coordinates to your Python session after clicking
def input_waypoints():
    while True:
        lat = input("Latitude (blank to end): ")
        if lat.strip() == "":
            break
        lon = input("Longitude: ")
        waypoints.append((float(lat), float(lon)))

    print("[INFO] Waypoints collected:")
    for wp in waypoints:
        print(wp)

# Call mission sender (to be implemented)
def send_mission():
    from mission_sender import send_mission
    send_mission(waypoints)

if __name__ == "__main__":
    generate_map()
    input_waypoints()
    send_mission()
