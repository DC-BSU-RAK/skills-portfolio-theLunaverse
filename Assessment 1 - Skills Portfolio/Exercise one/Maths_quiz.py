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

# === GIF Player Helper ===
class GIFPlayer:
    """Handles animated GIF playback on a label"""
    def __init__(self, label, gif_path, width, height):
        self.label = label # where the GIF will be shown
        self.frames = []  # store all frames of the GIF
        self.current_frame = 0
        self.job = None  # in order to stop the animation later
        
        # open the GIF file
        im = Image.open(gif_path)
        for frame in ImageSequence.Iterator(im): # go through each frame in GIF
            resized = frame.copy().resize((width, height), Image.LANCZOS) # LANCZOS from pillow for best quality 
            self.frames.append(ImageTk.PhotoImage(resized)) # resized the frame and convert it so Tkinter can show it

    def play(self):
        """Start playing the GIF from the beginning"""
        self.stop()
        self.current_frame = 0
        self.animate() # begin loop

    def animate(self):
        """Show next frame"""
        if self.frames:
            self.label.config(image=self.frames[self.current_frame]) # update the label image
            self.label.image = self.frames[self.current_frame]
            # move to next frame (loop back to 0 when done)
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            # show next frame in 40ms
            self.job = self.label.after(40, self.animate)

    def stop(self):
        """Stop the animation"""
        if self.job:  # check if an animation is running
            self.label.after_cancel(self.job)
            self.job = None

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