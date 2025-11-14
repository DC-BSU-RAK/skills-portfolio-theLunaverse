import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import random
import pygame
from modules.gif import GIFPlayer
from modules.constants import *

root = tk.Tk()
pygame.mixer.init()

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
        
        # punchline button - disabled until setup finishes
        self.btn_punchline = tk.Label(self.canvas, image=self.img_punchline_gray, bg=BG_COLOR, cursor="hand2")
        self.btn_punchline.place(x=SHOW_PUNCHLINE_BTN_X, y=BUTTON_Y, width=PUNCHLINE_WIDTH, height=PUNCHLINE_HEIGHT)
        
        # next joke button - only enabled after punchline is shown
        self.btn_next = tk.Label(self.canvas, image=self.img_next_gray, bg=BG_COLOR, cursor="hand2")
        self.btn_next.place(x=NEXT_JOKE_BTN_X, y=BUTTON_Y, width=NEXT_JOKE_WIDTH, height=NEXT_JOKE_HEIGHT)
        
        # quit button - always enabled
        self.btn_quit = tk.Label(self.canvas, image=self.img_quit, bg=BG_COLOR, cursor="hand2")
        self.btn_quit.place(x=QUIT_BTN_X, y=BUTTON_Y, width=QUIT_WIDTH, height=QUIT_HEIGHT)
        self.btn_quit.bind("<Button-1>", lambda e: self.quit())
        
        # mute button - controls music and sound effects
        self.btn_mute = tk.Label(self.canvas, image=self.img_mute, bg=BG_COLOR, cursor="hand2")
        self.btn_mute.place(x=MUTE_BTN_X, y=MUTE_BTN_Y, width=MUTE_WIDTH, height=MUTE_HEIGHT)
        self.btn_mute.bind("<Button-1>", lambda e: self.toggle_music())
        
        # === startup ===
        # show idle animation and start typewriter style text
        self.play_gif(self.gif_idle)
        self.is_typing = True
        self.play_music()
        self.start_typing()

    # === gif management ===
    def load_gifs(self):
        """load all GIFs into memory at startup"""
        # each GIF is preloaded so transitions are smooth
        self.gif_idle = GIFPlayer(self.label_bg, IDLE_GIF, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.gif_setup = GIFPlayer(self.label_bg, SETUP_GIF, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.gif_punch = GIFPlayer(self.label_bg, PUNCH_GIF, WINDOW_WIDTH, WINDOW_HEIGHT)

    def play_gif(self, gif):
        """stop all GIFs and play the specified one"""
        # ensures only one animation plays at a time
        GIFPlayer.stop_all()
        gif.play()

    # === image management ===
    def load_images(self):
        """load and resize all button images"""
        # tell joke button with enabled and disabled states
        img = Image.open(TELL_JOKE_IMG)
        img = img.resize((TELL_JOKE_WIDTH, TELL_JOKE_HEIGHT), Image.LANCZOS)
        self.img_tell = ImageTk.PhotoImage(img)
        # grayscale version indicates button is disabled
        self.img_tell_gray = ImageTk.PhotoImage(img.convert('L').convert('RGB'))
        
        # punchline button images
        img = Image.open(PUNCHLINE_IMG)
        img = img.resize((PUNCHLINE_WIDTH, PUNCHLINE_HEIGHT), Image.LANCZOS)
        self.img_punchline = ImageTk.PhotoImage(img)
        self.img_punchline_gray = ImageTk.PhotoImage(img.convert('L').convert('RGB'))
        
    # === typewriter text effects ===
    def start_typing(self):
        """start both Sans comment and initial dialogue animations simultaneously"""
        # Sans comment with sound effects
        self.type_sans(SANS_COMMENT)
        # initial dialogue is narrator (no sound effects)
        self.type_dialogue(INITIAL_DIALOGUE_MESSAGE, sans_speaking=False)
    # === music ===
    def play_music(self):
        """start background music on loop"""
        # load music file
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1) # -1 means infinite loop
        self.is_music_playing = True
        # show unmute icon to indicate music is playing
        self.btn_mute.config(image=self.img_mute)
    
root.mainloop()