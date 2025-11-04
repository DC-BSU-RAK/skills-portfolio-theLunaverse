import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import os

# === File Paths ===

# get the directory where this script is located
BASE_DIR = os.path.dirname(__file__)

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

# === Quiz Logic Functions ===
def random_int():
    """Generate a random number based on difficulty level"""
    if difficulty == "Easy":
        return random.randint(0, 9)  # single digit
    elif difficulty == "Moderate":
        return random.randint(10, 99)  # two digits
    else:
        return random.randint(1000, 9999)  # four digits

def decide_operation():
    """Randomly choose addition or subtraction"""
    return random.choice(['+', '-'])

def start_timer():
    """Start a 30-second countdown timer"""
    global time_remaining, timer_id
    time_remaining = 30  # reset the timer to 30 seconds
    update_timer()       # begin the countdown

def update_timer():
    """Update timer display and check if time is up"""
    global time_remaining, timer_id
    if time_remaining > 0:
        # change color to red when 10 seconds or less remain
        timer_label.config(text=f"TIME: {time_remaining}s", 
                        fg="#FF0000" if time_remaining <= 10 else "#FFA500")
        time_remaining -= 1
        timer_id = root.after(1000, update_timer)  # update every second by calling the function after 1 second
    else:
        time_up() # if timer hits 0, time-out

def stop_timer():
    """stop the countdown timer"""
    global timer_id
    if timer_id:
        root.after_cancel(timer_id) 
        timer_id = None

def time_up():
    """Handle when timer reaches zero"""
    num1, num2, op = current_question
    correct = num1 + num2 if op == '+' else num1 - num2
    feedback_label.config(text=f"TIME'S UP! ANSWER: {correct}", fg="red")
    disable_inputs() # shows 'time's up' and the correct answer
    root.after(2000, next_question)  # move to next question after 2 seconds

def start_quiz_with_difficulty(diff):
    """Start a new quiz with chosen difficulty"""
    global difficulty, score, question_count
    difficulty = diff
    score = 0 # reset score for new game
    question_count = 0 # reset question counter
    enable_inputs() # make sure inputs are active
    score_label.config(text=f"SCORE: {score}/100")
    show_frame(quiz_frame)
    
def show_frame(frame):
    """Switch to a different screen (menu, difficulty, or quiz)"""
    # stop all GIF animations
    menu_gif.stop()
    diff_gif.stop()
    hallow_gif.stop()
    jungle_gif.stop()
    crimson_gif.stop()
    
    # show the requested frame
    frame.tkraise()
    
    # start the GIF that belongs to the screen we are switching to
    if frame == menu_frame:
        menu_gif.play()
    elif frame == diff_frame:
        diff_gif.play()

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

# === Menu Frame ===
# create a label to hold background GIF
menu_bg = tk.Label(menu_frame)
menu_bg.pack(fill="both", expand=True) # make it fill the whole menu area
menu_gif = GIFPlayer(menu_bg, MENU_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# --- Start button ---
start_img = ImageTk.PhotoImage(Image.open(START_IMG_PATH).resize((280, 55), Image.LANCZOS))
start_button = tk.Label(menu_frame, image=start_img, bg="black", cursor="hand2") # create a label to act as a clickable Start button
start_button.image = start_img

# when clicked, switch to the difficulty selection frame
start_button.bind("<Button-1>", lambda e: show_frame(diff_frame))
start_button.place(relx=0.5, rely=0.59, anchor="center")

# --- Quit button ---
quit_img = ImageTk.PhotoImage(Image.open(QUIT_IMG_PATH).resize((280, 55), Image.LANCZOS))
quit_button = tk.Label(menu_frame, image=quit_img, bg="black", cursor="hand2") # clickable label
quit_button.image = quit_img
quit_button.bind("<Button-1>", lambda e: root.quit()) # when clicked, exit application
quit_button.place(relx=0.5, rely=0.75, anchor="center")

# === Difficulty Frame ===
# create the label that holds the background GIF
diff_bg = tk.Label(diff_frame)
diff_bg.pack(fill="both", expand=True) # fill entire menu screen
diff_gif = GIFPlayer(diff_bg, DIFF_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# Create three difficulty buttons (Easy, Moderate, Advanced)
for i, (text, y, diff) in enumerate([("Play", 147, "Easy"), ("Play", 250, "Moderate"), ("Play", 352, "Advanced")]):
    # create a label that acts like a button
    btn = tk.Label(diff_frame, text=text, font=("Comic Sans MS", 14, "bold"), 
                bg="#374a82", fg="white", cursor="hand2", padx=20, pady=8, relief=tk.RAISED, bd=2)
    btn.bind("<Button-1>", lambda e, d=diff: start_quiz_with_difficulty(d)) # start the quiz with chosen level when clicked
    btn.place(x=450, y=y)

# Back button
back_img = ImageTk.PhotoImage(Image.open(BACK_IMG_PATH).resize((280, 55), Image.LANCZOS))
back_button = tk.Label(diff_frame, image=back_img, bg="black", cursor="hand2") # create a label that works like a clickable Back button
back_button.image = back_img
back_button.bind("<Button-1>", lambda e: show_frame(menu_frame))
back_button.place(relx=0.5, rely=0.93, anchor="center")

# === Quiz Frame ===
# loading and placing all three background GIFs (one for each difficulty)

# easy
hallow_bg = tk.Label(quiz_frame)
hallow_bg.place(x=0, y=0, relwidth=1, relheight=1)
hallow_gif = GIFPlayer(hallow_bg, HALLOW_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# moderate 
jungle_bg = tk.Label(quiz_frame)
jungle_bg.place(x=0, y=0, relwidth=1, relheight=1)
jungle_gif = GIFPlayer(jungle_bg, JUNGLE_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# advanced
crimson_bg = tk.Label(quiz_frame)
crimson_bg.place(x=0, y=0, relwidth=1, relheight=1)
crimson_gif = GIFPlayer(crimson_bg, CRIMSON_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# back button (returns to diff menu)
quiz_back_img = ImageTk.PhotoImage(Image.open(BACK_IMG_PATH).resize((150, 40), Image.LANCZOS)) # create a label that acts as a Back button in the quiz screen
quiz_back_button = tk.Label(quiz_frame, image=quiz_back_img, bg="black", cursor="hand2")
quiz_back_button.image = quiz_back_img # keep a reference so the image doesn't disappear
quiz_back_button.bind("<Button-1>", lambda e: (stop_timer(), show_frame(diff_frame))) # stop timer when clicked and return to diff menu
quiz_back_button.place(x=20, y=20)

# question number label 
title_label = tk.Label(quiz_frame, font=("Comic Sans MS", 24, "bold"), fg="#FFD700", bg="#58386c")
title_label.place(relx=0.5, y=80, anchor="center")

# timer label
timer_label = tk.Label(quiz_frame, font=("Comic Sans MS", 16, "bold"), bg="#29356d", fg="#FFA500")
timer_label.place(relx=0.5, y=192, anchor="center")

# math question label
question_label = tk.Label(quiz_frame, font=("Comic Sans MS", 20, "bold"), bg="#131f44", fg="#FFFFFF")
question_label.place(relx=0.5, y=250, anchor="center")

# answer input area (container for entry box)
entry_frame = tk.Frame(quiz_frame, bg="#17242c")
entry_frame.place(relx=0.5, y=330, anchor="center")

# answer entry box
answer_entry = tk.Entry(entry_frame, font=("Comic Sans MS", 20, "bold"), width=10, 
                        bg="#17242c", fg="#FFFFFF", insertbackground="#FFFFFF", 
                        relief=tk.SOLID, bd=4, justify="center")
answer_entry.pack(side=tk.LEFT, padx=10)
answer_entry.bind('<Return>', lambda e: check_answer())  # allow Enter key to submit

# submit button
submit_btn = tk.Button(entry_frame, text="SUBMIT", font=("Comic Sans MS", 14, "bold"), 
                    command=check_answer, bg="#131f44", fg="#FFFFFF", # runs when the button is clicked
                    activebackground="#303072", relief=tk.RAISED, bd=4, 
                    cursor="hand2", padx=20, pady=12)
submit_btn.pack(side=tk.LEFT, padx=10) # place the button next to the entry box

# feedback label (shows correct/incorrect messages)
feedback_label = tk.Label(quiz_frame, font=("Comic Sans MS", 16, "bold"), bg="#585e8d", fg="#FFFFFF")
feedback_label.place(relx=0.5, y=425, anchor="center")

# score label
score_label = tk.Label(quiz_frame, font=("Comic Sans MS", 16, "bold"), bg="#585e8d", fg="#FFD700")
score_label.place(relx=0.5, y=455, anchor="center")

# start the application on the menu screen
show_frame(menu_frame)
root.mainloop()