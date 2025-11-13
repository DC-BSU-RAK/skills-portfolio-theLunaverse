import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import random
import pygame
from modules.gif import GIFPlayer
from modules.constants import *

root = tk.Tk()

class SansJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        
        # === initialiation ===
        self.jokes = self.load_jokes() # load jokes 
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)  # prevent window resizing
        self.current_joke = None  # stores the currently selected joke
        self.animation_text = None  # dialogue typewriter animation
        self.animation_comment = None  # sans comment typewriter animation
        self.is_typing = False  # prevents button clicks during typing
        self.is_music_playing = True  # tracks mute state
        self.button_enabled = {'punchline': False, 'next': False}  # track which buttons are clickable
        
        # === fonts ===
        self.dialogue_font = tkfont.Font(family=FONT_FAMILY, size=DIALOGUE_FONT_SIZE)
        self.sans_font = tkfont.Font(family=FONT_FAMILY, size=SANS_COMMENT_FONT_SIZE)
root.mainloop()