import folium
from folium.plugins import MousePosition
import webbrowser
import os

def create_map(center_lat=40.0, center_lon=29.0, zoom=17, save_file="waypoints.txt"):
    """
    Interactive map: click to select a point, press 's' to add as set point, 'd' to delete set point at that location.
    Waypoints are saved to file.
    """
    try:
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
        MousePosition().add_to(m)

        # Custom JS for keyboard-controlled set point add/delete
        custom_js = '''
        var waypoints = [];
        var markers = [];
        var markerLayer = L.layerGroup().addTo(map);
        var selectedLatLng = null;
        var tempMarker = null;

        function updateMarkers() {
            markerLayer.clearLayers();
            markers = [];
            for (var i = 0; i < waypoints.length; i++) {
                var wp = waypoints[i];
                var marker = L.marker([wp[0], wp[1]], {draggable: false});
                marker.bindTooltip((i+1).toString(), {permanent: true, direction: 'top'}).openTooltip();
                markerLayer.addLayer(marker);
                markers.push(marker);
            }
        }

        map.on('click', function(e) {
            selectedLatLng = e.latlng;
            if (tempMarker) {
                map.removeLayer(tempMarker);
            }
            tempMarker = L.marker([selectedLatLng.lat, selectedLatLng.lng], {icon: L.icon({iconUrl: 'https://maps.gstatic.com/mapfiles/ms2/micons/blue-dot.png', iconSize: [32,32], iconAnchor: [16,32]})});
            tempMarker.addTo(map);
        });

        document.addEventListener('keydown', function(event) {
            if (!selectedLatLng) return;
            if (event.key === 's') {
                // Add as set point if not already present
                var exists = false;
                for (var i = 0; i < waypoints.length; i++) {
                    if (Math.abs(waypoints[i][0] - selectedLatLng.lat) < 0.0001 && Math.abs(waypoints[i][1] - selectedLatLng.lng) < 0.0001) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    waypoints.push([selectedLatLng.lat, selectedLatLng.lng, 10.0]);
                    updateMarkers();
                }
            } else if (event.key === 'd') {
                // Delete set point at this location
                for (var i = 0; i < waypoints.length; i++) {
                    if (Math.abs(waypoints[i][0] - selectedLatLng.lat) < 0.0001 && Math.abs(waypoints[i][1] - selectedLatLng.lng) < 0.0001) {
                        waypoints.splice(i, 1);
                        updateMarkers();
                        break;
                    }
                }
            }
        });

        // Expose waypoints for export
        window.getWaypoints = function() { return waypoints; };
        '''
        m.get_root().html.add_child(folium.Element(f'<script>{custom_js}</script>'))

        map_file = "mission_map.html"
        m.save(map_file)

        abs_path = os.path.abspath(map_file)
        try:
            webbrowser.open(f"file://{abs_path}")
            print("[✓] Map opened in browser.")
        except Exception as e:
            print(f"[ERROR] Map could not be opened in browser: {e}")

        print("[→] Haritada bir noktaya sol tıklayın.\n's' tuşu ile set point ekleyin, 'd' tuşu ile o noktadaki set point'i silin.\nTüm noktaları seçtikten sonra harita sekmesini kapatın.")
        input("Set point seçimi bitince Enter'a basın...")

        # Kullanıcıdan waypoint'leri al
        print("Lütfen haritada eklediğiniz noktaların koordinatlarını (lat, lon, alt) sırayla girin.\nHer satıra bir nokta, bitince 'done' yazın:")
        user_waypoints = []
        while True:
            line = input()
            if line.strip().lower() == 'done':
                break
            try:
                parts = [float(x) for x in line.strip().split(",")]
                if len(parts) == 2:
                    parts.append(10.0)
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
