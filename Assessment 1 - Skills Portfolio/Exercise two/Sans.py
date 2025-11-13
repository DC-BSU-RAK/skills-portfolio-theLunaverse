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
        
        # preload all images before creating window
        self.load_images()
        
        # === canvas and background ===
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # background label holds the GIFs
        self.label_bg = tk.Label(self.canvas, bg=BG_COLOR)
        self.label_bg.place(x=0, y=0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        
        # load all GIF animations
        self.load_gifs()
        
        # === text boxes ===
        # sans comment box appears on startup 
        self.text_sans = tk.Text(
            self.canvas, font=self.sans_font, bg="#FFFFFF", fg="#000000", wrap="word",
            relief="flat", highlightthickness=0, padx=10, pady=10, spacing1=5,
            spacing2=SANS_COMMENT_SPACING, spacing3=5, state="disabled", cursor="arrow"
        )
        self.text_sans.place(x=SANS_COMMENT_X, y=SANS_COMMENT_Y, width=SANS_COMMENT_WIDTH, height=SANS_COMMENT_HEIGHT)
        
        # main dialogue box displays both narrator text and jokes
        self.label_dialogue = tk.Label(
            self.canvas, text="", font=self.dialogue_font, bg=BG_COLOR, fg="#FFFFFF",
            wraplength=DIALOGUE_WIDTH, justify="left", anchor="nw"
        )
        self.label_dialogue.place(x=DIALOGUE_X + INITIAL_TEXT_X_OFFSET, y=DIALOGUE_Y + DIALOGUE_TEXT_Y_OFFSET, width=DIALOGUE_WIDTH, height=DIALOGUE_TEXT_HEIGHT)
        
        # === buttons ===
        # tell joke button 
        self.btn_tell = tk.Label(self.canvas, image=self.img_tell, bg=BG_COLOR, cursor="hand2")
        self.btn_tell.place(x=TELL_JOKE_BTN_X, y=BUTTON_Y, width=TELL_JOKE_WIDTH, height=TELL_JOKE_HEIGHT)
        self.btn_tell.bind("<Button-1>", lambda e: self.tell_joke())
        
root.mainloop()