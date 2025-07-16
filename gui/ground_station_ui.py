import tkinter as tk
from control.auto_navigation import clear_mission, upload_mission, start_mission
from gui.waypoint_selector import create_map

def launch_gui(master):
    root = tk.Tk()
    root.title("Ground Station - Mission Control")

    # Label
    tk.Label(root, text="Enter 4 waypoint coordinates (lat, lon):").pack()

    # List of entry fields
    entries = []
    for i in range(4):
        frame = tk.Frame(root)
        frame.pack()
        lat_entry = tk.Entry(frame, width=15)
        lon_entry = tk.Entry(frame, width=15)
        lat_entry.pack(side="left", padx=5)
        lon_entry.pack(side="left", padx=5)
        entries.append((lat_entry, lon_entry))

    # Buttons
    def launch_map():
        create_map()

    def send_mission():
        waypoints = []
        for lat_e, lon_e in entries:
            try:
                lat = float(lat_e.get())
                lon = float(lon_e.get())
                waypoints.append((lat, lon, 5.0))  # Alt fixed at 5m
            except ValueError:
                print("[ERROR] Invalid coordinate.")
                return

        clear_mission(master)
        upload_mission(master, waypoints)
        start_mission(master)

    tk.Button(root, text="Open Map", command=launch_map).pack(pady=5)
    tk.Button(root, text="Send Mission", command=send_mission).pack(pady=5)

    # Live telemetry display
    telemetry_frame = tk.Frame(root)
    telemetry_frame.pack(pady=10)

    label_lat = tk.Label(telemetry_frame, text="Lat: ---")
    label_lon = tk.Label(telemetry_frame, text="Lon: ---")
    label_heading = tk.Label(telemetry_frame, text="Heading: ---")
    label_speed = tk.Label(telemetry_frame, text="Speed: ---")
    label_pwm1 = tk.Label(telemetry_frame, text="PWM CH1: ---")
    label_pwm2 = tk.Label(telemetry_frame, text="PWM CH2: ---")

    label_lat.pack()
    label_lon.pack()
    label_heading.pack()
    label_speed.pack()
    label_pwm1.pack()
    label_pwm2.pack()

    # Start telemetry update function
    update_telemetry(master, root, label_lat, label_lon, label_heading, label_speed, label_pwm1, label_pwm2)

    root.mainloop()

def update_telemetry(master, root, label_lat, label_lon, label_heading, label_speed, label_pwm1, label_pwm2):
    msg = master.recv_match(type=["GLOBAL_POSITION_INT", "VFR_HUD", "RC_CHANNELS"], blocking=False)
    
    if msg:
        if msg.get_type() == "GLOBAL_POSITION_INT":
            lat = msg.lat / 1e7
            lon = msg.lon / 1e7
            heading = msg.hdg / 100.0 if msg.hdg != 65535 else None
            label_lat.config(text=f"Lat: {lat:.6f}")
            label_lon.config(text=f"Lon: {lon:.6f}")
            if heading is not None:
                label_heading.config(text=f"Heading: {heading:.1f}\u00b0")

        elif msg.get_type() == "VFR_HUD":
            speed = msg.groundspeed
            label_speed.config(text=f"Speed: {speed:.2f} m/s")

        elif msg.get_type() == "RC_CHANNELS":
            label_pwm1.config(text=f"PWM CH1: {msg.chan1_raw}")
            label_pwm2.config(text=f"PWM CH2: {msg.chan2_raw}")
    
    # Schedule next update
    root.after(200, lambda: update_telemetry(master, root, label_lat, label_lon, label_heading, label_speed, label_pwm1, label_pwm2))
