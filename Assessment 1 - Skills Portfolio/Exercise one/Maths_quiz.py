import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from enum import Enum

from modules.gif import GIFPlayer, QuizFrame
from modules.constants import *

# === Difficulty Levels ===
class Difficulty(Enum):
    """Stores all difficulty settings in one place"""
    # format: (level, color, background_path, min_number, max_number)
    EASY = (0, "#58386c", HALLOW_GIF_PATH, 0, 9)  # single digit numbers
    MEDIUM = (1, "#2596be", JUNGLE_GIF_PATH, 10, 99)  # two digit numbers
    HARD = (2, "#896c57", CRIMSON_GIF_PATH, 1000, 9999)  # four digit numbers

    @property
    def level(self):
        """Get the difficulty level number"""
        return self.value[0]

    @property
    def color(self):
        """Get the background color for this difficulty"""
        return self.value[1]

    @property
    def path(self):
        """Get the GIF path for this difficulty"""
        return self.value[2]

    @property
    def min_val(self):
        """Get minimum number for this difficulty"""
        return self.value[3]

    @property
    def max_val(self):
        """Get maximum number for this difficulty"""
        return self.value[4]


# === Quiz State Management ===
class QuizContext:
    """Track quiz state throughout the application"""
    def __init__(self):
        self.difficulty = Difficulty.EASY  # current difficulty level
        self.score = 0  # current score (out of 100)
        self.question_count = 0  # number of questions answered
        self.current_question = None  # stores (num1, num2, operation)
        self.attempts = 0  # number of attempts on current question
        self.time_remaining = QUIZ_DURATION  # seconds remaining for current question
        self.timer_id = None  # reference to timer for cancellation

    def reset(self, new_difficulty=Difficulty.EASY):
        """Reset quiz state for a new game"""
        self.difficulty = new_difficulty
        self.score = 0
        self.question_count = 0
        self.current_question = None
        self.attempts = 0
        self.time_remaining = QUIZ_DURATION


# create single context instance to hold all state
Context = QuizContext()


# === Quiz Logic Functions ===
class QuizLogic:
    """Contains all the math quiz logic (separated from UI)"""
    
    @staticmethod
    def random_int(difficulty: Difficulty):
        """Generate a random number based on difficulty level"""
        return random.randint(difficulty.min_val, difficulty.max_val)

    @staticmethod
    def decide_operation():
        """Randomly choose addition or subtraction"""
        return random.choice(['+', '-'])

    @staticmethod
    def generate_problem(difficulty: Difficulty):
        """Generate a new math problem with two numbers and an operation"""
        num1 = QuizLogic.random_int(difficulty)
        num2 = QuizLogic.random_int(difficulty)
        op = QuizLogic.decide_operation()

        # for subtraction, ensure result is positive (except in Hard mode)
        if op == '-' and num1 < num2 and difficulty != Difficulty.HARD:
            num1, num2 = num2, num1

        return num1, num2, op

    @staticmethod
    def calculate_correct_answer(num1, num2, op):
        """Calculate the correct answer for a problem"""
        return num1 + num2 if op == '+' else num1 - num2

    @staticmethod
    def check_answer(num1, num2, op, user_answer):
        """Check if the given answer is correct"""
        return user_answer == QuizLogic.calculate_correct_answer(num1, num2, op)


# === Timer Functions ===
def start_timer():
    """Start a 30-second countdown timer"""
    Context.time_remaining = QUIZ_DURATION  # reset the timer to 30 seconds
    update_timer()  # begin the countdown

def update_timer():
    """Update timer display and check if time is up"""
    if Context.time_remaining >= 0:
        # change color to red when 10 seconds or less remain
        timer_label.config(
            text=f"TIME: {Context.time_remaining}s",
            fg="#FF0000" if Context.time_remaining <= 10 else "#FFA500"
        )
        Context.time_remaining -= 1
        # update every second by calling the function after 1 second
        Context.timer_id = root.after(1000, update_timer)
    else:
        time_up()  # if timer hits 0, time-out

def stop_timer():
    """Stop the countdown timer"""
    if Context.timer_id:
        root.after_cancel(Context.timer_id)
        Context.timer_id = None

def time_up():
    """Handle when timer reaches zero"""
    num1, num2, op = Context.current_question
    correct = QuizLogic.calculate_correct_answer(num1, num2, op)
    # shows 'time's up' and the correct answer
    feedback_label.config(text=f"TIME'S UP! ANSWER: {correct}", fg="red")
    disable_inputs()
    root.after(2000, next_question)  # move to next question after 2 seconds


# === Question Display Functions ===
def display_problem():
    """Generate and display a new math problem"""
    # generate a new problem based on current difficulty
    num1, num2, op = QuizLogic.generate_problem(Context.difficulty)

    # save the current question (numbers and operation)
    Context.current_question = (num1, num2, op)
    
    # update the question number at the top
    title_label.config(text=f"QUESTION {Context.question_count + 1}/{TOTAL_QUESTIONS}")
    
    # show the math problem
    question_label.config(text=f"{num1} {op} {num2} = ?")
    
    # clear any old feedback
    feedback_label.config(text="")
    
    # clear the answer box from any old answer
    answer_entry.delete(0, "end")
    
    # put cursor in answer box
    answer_entry.focus_set()
    
    # reset attempts counter
    Context.attempts = 0
    
    # start the countdown
    start_timer()


# === Answer Checking Functions ===
def check_answer():
    """Validate and score the user's answer"""
    stop_timer()  # pause timer while checking the answer
    
    # validate input is a number
    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        feedback_label.config(text="ENTER A VALID NUMBER!", fg="red")
        update_timer()  # restart timer because this wasn't a real attempt
        return

    num1, num2, op = Context.current_question

    # check if the answer is correct
    if QuizLogic.check_answer(num1, num2, op, user_answer):
        # award points: 10 for first try, 5 for second try
        points = 10 if Context.attempts == 0 else 5
        Context.score += points
        feedback_label.config(text=f"CORRECT! +{points} POINTS", fg="light green")
        disable_inputs()  # stop further typing
        root.after(1500, next_question)  # show next question after 1.5 seconds
    else:
        # if the answer is wrong
        Context.attempts += 1
        if Context.attempts < 2:
            # give user a second chance
            feedback_label.config(text="INCORRECT! TRY AGAIN!", fg="#FF4500")
            answer_entry.delete(0, "end")
            start_timer()
        else:
            # show correct answer after 2 failed attempts
            correct = QuizLogic.calculate_correct_answer(num1, num2, op)
            feedback_label.config(text=f"INCORRECT! ANSWER: {correct}", fg="orange")
            disable_inputs()
            root.after(2000, next_question)  # move on after 2 seconds

    # update the score display at the top of the screen
    score_label.config(text=f"SCORE: {Context.score}/{10 * TOTAL_QUESTIONS}")


# === Input Control Functions ===
def disable_inputs():
    """Prevent user from entering answer (during feedback)"""
    answer_entry.config(state="disabled")
    submit_btn.config(state="disabled")

def enable_inputs():
    """Allow user to enter answer"""
    answer_entry.config(state="normal")
    submit_btn.config(state="normal")


# === Question Navigation Functions ===
def next_question():
    """Move to the next question or show results if quiz is complete"""
    stop_timer()
    Context.question_count += 1
    if Context.question_count < TOTAL_QUESTIONS:
        enable_inputs()
        display_problem()
    else:
        display_results()


# === Quiz Start/End Functions ===
def start_quiz_with_difficulty(diff):
    """Start a new quiz with chosen difficulty"""
    # reset all state for new game
    Context.reset(diff)
    
    # make sure inputs are active
    enable_inputs()
    
    # reset score display
    score_label.config(text=f"SCORE: {Context.score}/{10 * TOTAL_QUESTIONS}")
    
    # switch to quiz screen
    show_frame(quiz_frame)

    # get or create the background for this difficulty and show it
    QuizFrame.get_or_create(quiz_frame, diff).start()

    # bring all quiz elements to front using lift
    quiz_back_button.lift()
    title_label.lift()
    timer_label.lift()
    question_label.lift()
    entry_frame.lift()
    feedback_label.lift()
    score_label.lift()

    # show first question
    display_problem()

def display_results():
    """Show final score and grade, ask to play again"""
    stop_timer()  # make sure the timer is not running

    # calculate final score
    max_score = 10 * TOTAL_QUESTIONS
    score = Context.score

    # calculate letter grade based on score
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    message = f"FINAL SCORE: {score}/{max_score}\nGRADE: {grade}\n\nPlay again?"

    # ask the user if they want to restart the quiz
    if messagebox.askyesno("Quiz Complete!", message):
        show_frame(menu_frame)  # if they say yes → return to the main menu
    else:
        root.quit()  # if they say no → close the program


# === Frame Switching Functions ===
def show_frame(frame):
    """Switch to a different screen (menu, difficulty, or quiz)"""
    # stop all GIF animations
    GIFPlayer.stop_all()
    
    # show the requested frame
    frame.tkraise()
    
    # start the GIF that belongs to the screen we are switching to
    if frame == menu_frame:
        menu_gif.play()
    elif frame == diff_frame:
        diff_gif.play()


# === App ===
# create main window
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
menu_bg.pack(fill="both", expand=True)  # make it fill the whole menu area
menu_gif = GIFPlayer(menu_bg, MENU_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# --- Start button ---
start_img = ImageTk.PhotoImage(Image.open(START_IMG_PATH).resize((280, 55), Image.LANCZOS))
start_button = tk.Label(menu_frame, image=start_img, bg="black", cursor="hand2")  # create a label to act as a clickable Start button
start_button.image = start_img  # keep a reference so the image doesn't disappear

# when clicked, switch to the difficulty selection frame
start_button.bind("<Button-1>", lambda e: show_frame(diff_frame))
start_button.place(relx=0.5, rely=0.59, anchor="center")

# --- Quit button ---
quit_img = ImageTk.PhotoImage(Image.open(QUIT_IMG_PATH).resize((280, 55), Image.LANCZOS))
quit_button = tk.Label(menu_frame, image=quit_img, bg="black", cursor="hand2")  # clickable label
quit_button.image = quit_img  # keep a reference so the image doesn't disappear
quit_button.bind("<Button-1>", lambda e: root.quit())  # when clicked, exit application
quit_button.place(relx=0.5, rely=0.75, anchor="center")


# === Difficulty Frame ===
# create the label that holds the background GIF
diff_bg = tk.Label(diff_frame)
diff_bg.pack(fill="both", expand=True)  # fill entire menu screen
diff_gif = GIFPlayer(diff_bg, DIFF_GIF_PATH, WINDOW_WIDTH, WINDOW_HEIGHT)

# create three difficulty buttons (Easy, Moderate, Advanced)
for i, (text, y, diff) in enumerate([
    ("Play", 147, Difficulty.EASY),
    ("Play", 250, Difficulty.MEDIUM),
    ("Play", 352, Difficulty.HARD)
]):
    # create a label that acts like a button
    btn = tk.Label(diff_frame, text=text, font=("Comic Sans MS", 14, "bold"),
                bg="#374a82", fg="white", cursor="hand2", padx=20, pady=8, relief=tk.RAISED, bd=2)
    btn.bind("<Button-1>", lambda e, d=diff: start_quiz_with_difficulty(d))  # start the quiz with chosen level when clicked
    btn.place(x=450, y=y)

# --- Back button ---
back_img = ImageTk.PhotoImage(Image.open(BACK_IMG_PATH).resize((280, 55), Image.LANCZOS))
back_button = tk.Label(diff_frame, image=back_img, bg="black", cursor="hand2")  # create a label that works like a clickable Back button
back_button.image = back_img  # keep a reference so the image doesn't disappear
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