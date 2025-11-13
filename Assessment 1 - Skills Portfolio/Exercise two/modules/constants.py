import os

# === file Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
JOKES_FILE_PATH = os.path.join(BASE_DIR, "media", "randomJokes.txt")

# === window Settings ===
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
WINDOW_TITLE = "sans. - Joke Teller"
# === dialogue Box ===
DIALOGUE_X = 160
DIALOGUE_Y = 125
DIALOGUE_WIDTH = 700
DIALOGUE_HEIGHT = 160

# === sans's comment box ===
SANS_COMMENT_X = 655
SANS_COMMENT_Y = 51
SANS_COMMENT_WIDTH = 170
SANS_COMMENT_HEIGHT = 165
SANS_COMMENT_SPACING = 10
# === font Settings ===
FONT_FAMILY = "Comic Sans MS"
DIALOGUE_FONT_SIZE = 30
SANS_COMMENT_FONT_SIZE = 19
SANS_COMMENT = 'You really should press that \n"tell me a joke" button, y\'know?'