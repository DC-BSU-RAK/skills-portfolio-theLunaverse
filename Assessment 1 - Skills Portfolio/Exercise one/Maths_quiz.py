import tkinter as tk
from tkinter import messagebox
import random

# === Quiz Logic Functions ===


def start_timer():
    """Start a 30-second countdown timer"""

def update_timer():
    """Update timer display and check if time is up"""
        # change color to red when 10 seconds or less remain
    else:

def stop_timer():

def time_up():
    """Handle when timer reaches zero"""
    feedback_label.config(text=f"TIME'S UP! ANSWER: {correct}", fg="red")
    root.after(2000, next_question)  # move to next question after 2 seconds

def display_problem():
    """Generate and display a new math problem"""
    
    
    question_label.config(text=f"{num1} {op} {num2} = ?")
    feedback_label.config(text="")
    start_timer()


def check_answer():
    """Validate and score the user's answer"""
    
    # validate input is a number
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        feedback_label.config(text="ENTER A VALID NUMBER!", fg="red")
        return

        # award points: 10 for first try, 5 for second try
        feedback_label.config(text=f"CORRECT! +{points} POINTS", fg="light green")
    else:
            # give user a second chance
            feedback_label.config(text="INCORRECT! TRY AGAIN!", fg="#FF4500")
            answer_entry.delete(0, "end")
            start_timer()
        else:
            # show correct answer after 2 failed attempts
            feedback_label.config(text=f"INCORRECT! ANSWER: {correct}", fg="orange")
            disable_inputs()
    # update the score display at the top of the screen

def disable_inputs():
    """Prevent user from entering answer (during feedback)"""
    answer_entry.config(state="disabled")
    submit_btn.config(state="disabled")

def enable_inputs():
    """Allow user to enter answer"""
    answer_entry.config(state="normal")
    submit_btn.config(state="normal")

def next_question():
    """Move to the next question or show results if quiz is complete"""
    stop_timer()
        enable_inputs()
        display_problem()
    else:
        display_results()

def start_quiz_with_difficulty(diff):
    """Start a new quiz with chosen difficulty"""
    
    
    # bring all quiz elements to front using lift
    quiz_back_button.lift()
    title_label.lift()
    timer_label.lift()
    question_label.lift()
    entry_frame.lift()
    feedback_label.lift()
    score_label.lift()
    display_problem()

def display_results():
    """Show final score and grade, ask to play again"""
    # calculate letter grade based on score

    # ask the user if they want to restart the quiz
    else:
def show_frame(frame):
    """Switch to a different screen (menu, difficulty, or quiz)"""
    # stop all GIF animations
    
    # show the requested frame
    frame.tkraise()
    
    # start the GIF that belongs to the screen we are switching to
    if frame == menu_frame:
        menu_gif.play()
    elif frame == diff_frame:
        diff_gif.play()

# === App ===
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
menu_gif = GIFPlayer(menu_bg, MENU_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# --- Start button ---
start_img = ImageTk.PhotoImage(Image.open(START_IMG_PATH).resize((280, 55), Image.LANCZOS))

# when clicked, switch to the difficulty selection frame
start_button.bind("<Button-1>", lambda e: show_frame(diff_frame))
start_button.place(relx=0.5, rely=0.59, anchor="center")

# --- Quit button ---
quit_img = ImageTk.PhotoImage(Image.open(QUIT_IMG_PATH).resize((280, 55), Image.LANCZOS))
quit_button.place(relx=0.5, rely=0.75, anchor="center")

# === Difficulty Frame ===
# create the label that holds the background GIF
diff_bg = tk.Label(diff_frame)
diff_gif = GIFPlayer(diff_bg, DIFF_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

    # create a label that acts like a button
                bg="#374a82", fg="white", cursor="hand2", padx=20, pady=8, relief=tk.RAISED, bd=2)
    btn.place(x=450, y=y)

back_img = ImageTk.PhotoImage(Image.open(BACK_IMG_PATH).resize((280, 55), Image.LANCZOS))
back_button.bind("<Button-1>", lambda e: show_frame(menu_frame))
back_button.place(relx=0.5, rely=0.93, anchor="center")

# === Quiz Frame ===
quiz_back_button.place(x=20, y=20)

title_label.place(relx=0.5, y=80, anchor="center")

timer_label = tk.Label(quiz_frame, font=("Comic Sans MS", 16, "bold"), bg="#29356d", fg="#FFA500")
timer_label.place(relx=0.5, y=192, anchor="center")

question_label = tk.Label(quiz_frame, font=("Comic Sans MS", 20, "bold"), bg="#131f44", fg="#FFFFFF")
question_label.place(relx=0.5, y=250, anchor="center")

entry_frame = tk.Frame(quiz_frame, bg="#17242c")
entry_frame.place(relx=0.5, y=330, anchor="center")

                        relief=tk.SOLID, bd=4, justify="center")
answer_entry.pack(side=tk.LEFT, padx=10)
answer_entry.bind('<Return>', lambda e: check_answer())  # allow Enter key to submit

                    cursor="hand2", padx=20, pady=12)

feedback_label = tk.Label(quiz_frame, font=("Comic Sans MS", 16, "bold"), bg="#585e8d", fg="#FFFFFF")
feedback_label.place(relx=0.5, y=425, anchor="center")

score_label = tk.Label(quiz_frame, font=("Comic Sans MS", 16, "bold"), bg="#585e8d", fg="#FFD700")
score_label.place(relx=0.5, y=455, anchor="center")

# start the application on the menu screen
show_frame(menu_frame)
root.mainloop()