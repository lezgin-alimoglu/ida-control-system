import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, pyqtSignal
import os

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Waypoint Selector</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <style> #map { height: 100vh; width: 100vw; } </style>
</head>
<body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
<script>
var map = L.map('map').setView([40.0, 29.0], 17);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

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
                window.pyObj && window.pyObj.onWaypointsChanged(JSON.stringify(waypoints));
            }
        })(i));
        markerLayer.addLayer(marker);
        markers.push(marker);
    }
    window.pyObj && window.pyObj.onWaypointsChanged(JSON.stringify(waypoints));
}

map.on('click', function(e) {
    waypoints.push([e.latlng.lat, e.latlng.lng, 10.0]);
    updateMarkers();
});

window.getWaypoints = function() { return waypoints; };
</script>
</body>
</html>
'''

class Bridge(QObject):
    waypointsChanged = pyqtSignal(str)

    @pyqtSlot(str)
    def onWaypointsChanged(self, waypoints_json):
        self.waypointsChanged.emit(waypoints_json)

class WaypointSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Waypoint Selector (PyQt5)")
        self.resize(900, 700)
        self.waypoints = []

        self.web = QWebEngineView()
        self.bridge = Bridge()
        self.bridge.waypointsChanged.connect(self.on_waypoints_changed)

        # Save HTML to temp file
        self.html_path = os.path.abspath("waypoint_selector_temp.html")
        with open(self.html_path, "w") as f:
            f.write(HTML_TEMPLATE)
        self.web.load(QUrl.fromLocalFile(self.html_path))

        # Expose bridge to JS
        self.web.page().setWebChannel(None)
        self.web.page().runJavaScript(
            "window.pyObj = {onWaypointsChanged: function(wp) { qt.bridge.onWaypointsChanged(wp); }};"
        )
        self.web.page().webChannel().registerObject('bridge', self.bridge)

        # Save button
        self.save_btn = QPushButton("Kaydet ve Kapat")
        self.save_btn.clicked.connect(self.save_and_close)

        layout = QVBoxLayout()
        layout.addWidget(self.web)
        layout.addWidget(self.save_btn)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @pyqtSlot(str)
    def on_waypoints_changed(self, waypoints_json):
        import json
        self.waypoints = json.loads(waypoints_json)

    def save_and_close(self):
        if not self.waypoints:
            QMessageBox.warning(self, "Uyarı", "Hiç waypoint eklenmedi!")
            return
        with open("waypoints.txt", "w") as f:
            for wp in self.waypoints:
                f.write(f"{wp[0]},{wp[1]},{wp[2]}\n")
        QMessageBox.information(self, "Başarılı", f"{len(self.waypoints)} waypoint kaydedildi!")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WaypointSelector()
    win.show()
    sys.exit(app.exec_()) 