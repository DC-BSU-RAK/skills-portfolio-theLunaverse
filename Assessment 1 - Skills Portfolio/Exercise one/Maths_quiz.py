import tkinter as tk
import os

# === File Paths ===

# get the directory where this script is located
BASE_DIR = os.path.dirname(__file__)

# getting paths to all media files (backgrounds and buttons) using os.path.join
MENU_GIF_PATH = os.path.join(BASE_DIR, "media", "menu_wp.gif")
START_IMG_PATH = os.path.join(BASE_DIR, "media", "start_btn.png")
QUIT_IMG_PATH = os.path.join(BASE_DIR, "media", "quit_btn.png")
# === Settings ===
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
# === App ===
root = tk.Tk()
root.title("Maths Quiz")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.mainloop()
