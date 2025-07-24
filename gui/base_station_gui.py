import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import threading
import time
import subprocess
from math import sin, cos, radians
from comm.jetson_comm import send_command_pwm



# === COORDINATE BOUNDS OF THE MAP IMAGE ===
# Adjust these to match your map.png
MIN_LAT, MAX_LAT = 39.81927, 39.83423
MIN_LON, MAX_LON = 32.81857, 32.85107 


MAP_WIDTH, MAP_HEIGHT = 800, 600  # size of map.png

# === HELPER FUNCTIONS ===
def pixel_to_coord(x, y):
    lon = MIN_LON + (x / MAP_WIDTH) * (MAX_LON - MIN_LON)
    lat = MAX_LAT - (y / MAP_HEIGHT) * (MAX_LAT - MIN_LAT)
    return round(lat, 6), round(lon, 6)

def read_position():
    try:
        with open("position.json", "r") as f:
            pos = json.load(f)
            return pos["lat"], pos["lon"], pos["yaw"]
    except:
        return None


def coord_to_pixel(lat, lon):
    x = int((lon - MIN_LON) / (MAX_LON - MIN_LON) * MAP_WIDTH)
    y = int((MAX_LAT - lat) / (MAX_LAT - MIN_LAT) * MAP_HEIGHT)
    return x, y

# === GUI CLASS ===
class USV_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("USV Base Station (Tkinter)")
        self.waypoints = []

        self.map_img = Image.open("map.png").resize((MAP_WIDTH, MAP_HEIGHT))
        self.map_photo = ImageTk.PhotoImage(self.map_img)

        self.canvas = tk.Canvas(root, width=MAP_WIDTH, height=MAP_HEIGHT)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.map_photo, anchor=tk.NW)
        
        self.bot_shape = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill="red")

        self.canvas.bind("<Button-1>", self.on_click)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save Mission", command=self.save_mission).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear Waypoints", command=self.clear_waypoints).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Göreve Başla", command=self.start_mission).pack(side=tk.LEFT, padx=5) 
        tk.Button(btn_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)


        # Start GPS update loop in separate thread
        self.running = True
        threading.Thread(target=self.update_bot_loop, daemon=True).start()

    def on_click(self, event):
        lat, lon = pixel_to_coord(event.x, event.y)
        self.waypoints.append((lat, lon))
        self.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, fill="blue")
        self.canvas.create_text(event.x+10, event.y, text=f"{len(self.waypoints)}", fill="white", font=("Arial", 10, "bold"))

    def save_mission(self):
        with open("mission.txt", "w") as f:
            for lat, lon in self.waypoints:
                f.write(f"{lat},{lon}\n")
        messagebox.showinfo("Mission Saved", f"{len(self.waypoints)} waypoint kaydedildi.")

    def clear_waypoints(self):
        self.waypoints.clear()
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.map_photo, anchor=tk.NW)

    def update_bot_loop(self):
        while self.running:
            pos = read_position()
            if pos:
                lat, lon = pos[:2]
                yaw = pos[2]  

                x, y = coord_to_pixel(lat, lon)
                r = 10  
                angle_rad = radians(-yaw)  

                # Üçgenin üç köşesini hesapla
                p1 = (x + r * cos(angle_rad), y + r * sin(angle_rad))  # ileri yön
                p2 = (x + r * cos(angle_rad + 2.5), y + r * sin(angle_rad + 2.5))  # sol arka
                p3 = (x + r * cos(angle_rad - 2.5), y + r * sin(angle_rad - 2.5))  # sağ arka

                self.canvas.coords(self.bot_shape, *p1, *p2, *p3)

            time.sleep(1)


    def stop(self):
        self.running = False

    def start_mission(self):
        self.save_mission()  
        messagebox.showinfo("Mission", "Mission started...")
        subprocess.Popen(["python3", "control/auto_nav.py"]) 


# === MAIN ===
if __name__ == "__main__":
    root = tk.Tk()
    gui = USV_GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.stop)
    root.mainloop()
