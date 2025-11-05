# === constants.py ===
import os

# === File Paths ===

# get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# getting paths to all media files (backgrounds and buttons) using os.path.join
MENU_GIF_PATH = os.path.join(BASE_DIR, "media", "menu_wp.gif")
DIFF_GIF_PATH = os.path.join(BASE_DIR, "media", "diff_wp.gif")
HALLOW_GIF_PATH = os.path.join(BASE_DIR, "media", "hallow_wp.gif")
JUNGLE_GIF_PATH = os.path.join(BASE_DIR, "media", "jungle_wp.gif")
CRIMSON_GIF_PATH = os.path.join(BASE_DIR, "media", "crimson_wp.gif")
START_IMG_PATH = os.path.join(BASE_DIR, "media", "start_btn.png")
QUIT_IMG_PATH = os.path.join(BASE_DIR, "media", "quit_btn.png")
BACK_IMG_PATH = os.path.join(BASE_DIR, "media", "back_btn.png")

# === Settings ===
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
QUIZ_DURATION = 30  # seconds for each question
TOTAL_QUESTIONS = 10  # number of questions per quiz