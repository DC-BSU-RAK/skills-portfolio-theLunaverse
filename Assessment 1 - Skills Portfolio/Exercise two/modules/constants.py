import os

# === file Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JOKES_FILE_PATH = os.path.join(BASE_DIR, "media", "randomJokes.txt")

# background GIFs
IDLE_GIF = os.path.join(BASE_DIR, "media", "sans_start.gif")
SETUP_GIF = os.path.join(BASE_DIR, "media", "sans_joke.gif")
PUNCH_GIF = os.path.join(BASE_DIR, "media", "sans_punchline.gif")

# button Images
TELL_JOKE_IMG = os.path.join(BASE_DIR, "media", "tell_joke.png")
PUNCHLINE_IMG = os.path.join(BASE_DIR, "media", "punchline.png")
NEXT_JOKE_IMG = os.path.join(BASE_DIR, "media", "next_joke.png")
QUIT_IMG = os.path.join(BASE_DIR, "media", "quit.png")

# === window Settings ===
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
WINDOW_TITLE = "sans. - Joke Teller"

# music
MUSIC_PATH = os.path.join(BASE_DIR, "media", "sans..mp3")

# mute button
MUTE_IMG = os.path.join(BASE_DIR, "media", "mute.png")
UNMUTE_IMG = os.path.join(BASE_DIR, "media", "unmute.png")
MUTE_WIDTH = 40
MUTE_HEIGHT = 40
MUTE_BTN_X = 20
MUTE_BTN_Y = 20

# === dialogue Box ===
DIALOGUE_X = 160
DIALOGUE_Y = 125
DIALOGUE_WIDTH = 700
DIALOGUE_HEIGHT = 160

# text position within dialogue box
DIALOGUE_TEXT_Y_OFFSET = 170
DIALOGUE_TEXT_HEIGHT = 100
DIALOGUE_TEXT_X_OFFSET = 50
INITIAL_TEXT_X_OFFSET = -50

# === sans's comment box ===
SANS_COMMENT_X = 655
SANS_COMMENT_Y = 51
SANS_COMMENT_WIDTH = 170
SANS_COMMENT_HEIGHT = 165
SANS_COMMENT_SPACING = 10

# === button positioning ===
BUTTON_Y = 478

# button sizes
TELL_JOKE_WIDTH = 260
TELL_JOKE_HEIGHT = 57
PUNCHLINE_WIDTH = 288
PUNCHLINE_HEIGHT = 58
NEXT_JOKE_WIDTH = 190
NEXT_JOKE_HEIGHT = 58
QUIT_WIDTH = 170
QUIT_HEIGHT = 57

# button X positions
TELL_JOKE_BTN_X = 20
SHOW_PUNCHLINE_BTN_X = TELL_JOKE_BTN_X + TELL_JOKE_WIDTH + 5
NEXT_JOKE_BTN_X = SHOW_PUNCHLINE_BTN_X + PUNCHLINE_WIDTH + 5
QUIT_BTN_X = NEXT_JOKE_BTN_X + NEXT_JOKE_WIDTH + 5

# === font Settings ===
FONT_FAMILY = "Comic Sans MS"
DIALOGUE_FONT_SIZE = 30
SANS_COMMENT_FONT_SIZE = 19
# === colors ===
BG_COLOR = "#000000"
DIALOGUE_TEXT_COLOR = "#000000"

# === text content ===
INITIAL_DIALOGUE_MESSAGE = "Sans looks like he's about to tell you a joke"
SANS_COMMENT = 'You really should press that \n"tell me a joke" button, y\'know?'