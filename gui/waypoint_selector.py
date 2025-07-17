import folium
from folium.plugins import MousePosition
import webbrowser
import os

def create_map(center_lat=40.0, center_lon=29.0, zoom=17, save_file="waypoints.txt"):
    """
    Creates an interactive map where right-click adds a numbered marker as a waypoint,
    and right-clicking again on a marker removes it. Waypoints are saved to file.
    """
    try:
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
        MousePosition().add_to(m)

        # Custom JS for right-click add/remove numbered markers
        custom_js = '''
        var waypoints = [];
        var markers = [];
        var markerLayer = L.layerGroup().addTo(map);

        function updateMarkers() {
            markerLayer.clearLayers();
            markers = [];
            for (var i = 0; i < waypoints.length; i++) {
                var wp = waypoints[i];
                var marker = L.marker([wp[0], wp[1]], {draggable: false});
                marker.bindTooltip((i+1).toString(), {permanent: true, direction: 'top'}).openTooltip();
                marker.on('contextmenu', (function(idx) {
                    return function(e) {
                        waypoints.splice(idx, 1);
                        updateMarkers();
                    }
                })(i));
                markerLayer.addLayer(marker);
                markers.push(marker);
            }
        }

        map.on('contextmenu', function(e) {
            // Check if clicked on an existing marker (within 0.0001 deg)
            var found = false;
            for (var i = 0; i < waypoints.length; i++) {
                var wp = waypoints[i];
                if (Math.abs(wp[0] - e.latlng.lat) < 0.0001 && Math.abs(wp[1] - e.latlng.lng) < 0.0001) {
                    // Remove this marker
                    waypoints.splice(i, 1);
                    updateMarkers();
                    found = true;
                    break;
                }
            }
            if (!found) {
                waypoints.push([e.latlng.lat, e.latlng.lng, 10.0]);
                updateMarkers();
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

        print("[→] Sağ tık ile set point ekleyin. Aynı noktaya tekrar sağ tıklarsanız o set point silinir.\nTüm noktaları seçtikten sonra harita sekmesini kapatın.")
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
