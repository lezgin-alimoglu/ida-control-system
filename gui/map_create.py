from urllib.parse import urlparse, parse_qs
import math

def extract_lat_lon_zoom(url):
    if "#map=" not in url:
        raise ValueError("URL must contain #map= section")

    _, map_params = url.split("#map=")
    zoom_str, lat_str, lon_str = map_params.split("/")
    return int(zoom_str), float(lat_str), float(lon_str)

def calculate_bbox(lat, lon, zoom, width=1280, height=960):
    # Constants
    TILE_SIZE = 256
    initial_resolution = 2 * math.pi * 6378137 / TILE_SIZE
    origin_shift = 2 * math.pi * 6378137 / 2.0

    def latlon_to_meters(lat, lon):
        mx = lon * origin_shift / 180.0
        my = math.log(math.tan((90 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
        my = my * origin_shift / 180.0
        return mx, my

    def meters_to_latlon(mx, my):
        lon = (mx / origin_shift) * 180.0
        lat = (my / origin_shift) * 180.0
        lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return lat, lon

    res = initial_resolution / (2 ** zoom)
    mx, my = latlon_to_meters(lat, lon)

    dx = width / 2 * res
    dy = height / 2 * res

    minx = mx - dx
    maxx = mx + dx
    miny = my - dy
    maxy = my + dy

    min_lat, min_lon = meters_to_latlon(minx, miny)
    max_lat, max_lon = meters_to_latlon(maxx, maxy)

    return min_lon, min_lat, max_lon, max_lat

def generate_staticmap_url(url, width=1280, height=960):
    zoom, lat, lon = extract_lat_lon_zoom(url)
    bbox = calculate_bbox(lat, lon, zoom, width, height)
    bbox_str = ",".join(f"{val:.6f}" for val in bbox)
    return f"https://staticmap.openstreetmap.de/staticmap.php?bbox={bbox_str}&size={width}x{height}"

# === Example ===
osm_url = "https://www.openstreetmap.org/#map=18/39.869626/32.775744"
staticmap_url = generate_staticmap_url(osm_url, width=1280, height=960)
print("[✓] StaticMap URL:", staticmap_url)
