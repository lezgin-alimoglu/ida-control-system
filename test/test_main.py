import time
import json

# Example path with simulated yaw values
fake_path = [
    (39.9020, 32.7520, 0),
    (39.9025, 32.7530, 45),
    (39.9030, 32.7540, 90),
    (39.9035, 32.7550, 135),
    (39.9040, 32.7560, 180),
]

i = 0

while True:
    lat, lon, yaw = fake_path[i % len(fake_path)]
    data = {
        "lat": lat,
        "lon": lon,
        "yaw": yaw
    }

    with open("position.json", "w") as f:
        json.dump(data, f)

    print(f"[TEST] Position updated: {lat}, {lon}, yaw: {yaw}")
    i += 1
    time.sleep(1)
