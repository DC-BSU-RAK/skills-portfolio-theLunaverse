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

# === Global Variables ===
# track quiz state throughout the application, starter variables are :
difficulty = "Easy"  # current difficulty level
score = 0  # current score (out of 100)
question_count = 0  # number of questions answered
current_question = None  # stores (num1, num2, operation)
attempts = 0  # number of attempts on current question
time_remaining = 30  # seconds remaining for current question
timer_id = None  # reference to timer for cancellation

# === App ===
# Create main window
root = tk.Tk()
root.title("Maths Quiz")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

# create three main frames (screens)
menu_frame = tk.Frame(root, bg="black")
diff_frame = tk.Frame(root, bg="black")
quiz_frame = tk.Frame(root, bg="black")

# place all frames in same position (only one visible at a time)
for f in (menu_frame, diff_frame, quiz_frame):
    f.place(relwidth=1, relheight=1)

root.mainloop()