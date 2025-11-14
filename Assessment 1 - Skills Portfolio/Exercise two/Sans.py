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
        
        # next joke button images
        img = Image.open(NEXT_JOKE_IMG)
        img = img.resize((NEXT_JOKE_WIDTH, NEXT_JOKE_HEIGHT), Image.LANCZOS)
        self.img_next = ImageTk.PhotoImage(img)
        self.img_next_gray = ImageTk.PhotoImage(img.convert('L').convert('RGB'))
        
        # quit button - no disabled state needed
        img = Image.open(QUIT_IMG)
        img = img.resize((QUIT_WIDTH, QUIT_HEIGHT), Image.LANCZOS)
        self.img_quit = ImageTk.PhotoImage(img)
        
        # mute button has two states - one for music on, one for music off
        img = Image.open(UNMUTE_IMG)
        img = img.resize((MUTE_WIDTH, MUTE_HEIGHT), Image.LANCZOS)
        self.img_mute = ImageTk.PhotoImage(img)  # shows when music is playing
        
        img = Image.open(MUTE_IMG)
        img = img.resize((MUTE_WIDTH, MUTE_HEIGHT), Image.LANCZOS)
        self.img_unmute = ImageTk.PhotoImage(img)  # shows when music is muted
    
    # === typewriter text effects ===
    def start_typing(self):
        """start both Sans comment and initial dialogue animations simultaneously"""
        # Sans comment with sound effects
        self.type_sans(SANS_COMMENT)
        # initial dialogue is narrator (no sound effects)
        self.type_dialogue(INITIAL_DIALOGUE_MESSAGE, sans_speaking=False)
    
    def type_sans(self, text, index=0):
        """animate Sans comment box character by character with sound"""
        if index <= len(text):
            # update text box with next character
            self.text_sans.config(state="normal")
            self.text_sans.delete("1.0", "end")
            self.text_sans.insert("1.0", text[:index])
            self.text_sans.config(state="disabled")
            
            # play talking sound for each letter if music is enabled
            # skip spaces to avoid extra sounds
            if self.is_music_playing and index > 0 and text[index - 1] != ' ':
                try:
                    pygame.mixer.Sound(LETTER_SOUND_PATH).play()
                except:
                    pass  # continue if sound fails to play
            
            # schedule next character after delay using animation_comment to store the scheduled task
            self.animation_comment = self.root.after(TYPEWRITER_SPEED, self.type_sans, text, index + 1)
    
    def type_dialogue(self, text, index=0, callback=None, sans_speaking=False):
        """animate dialogue box character by character"""
        if index <= len(text):
            # update dialogue with next character
            self.label_dialogue.config(text=text[:index])
            
            # only play sound if Sans is speaking (not narrator)
            # skip punctuation to avoid sound effects on punctuation marks
            if sans_speaking and self.is_music_playing and index > 0 and text[index - 1] not in ' .,!?':
                try:
                    pygame.mixer.Sound(LETTER_SOUND_PATH).play()
                except:
                    pass  # continue if sound fails to play
            
            # schedule next character after delay using animation_text to store the scheduled task
            self.animation_text = self.root.after(TYPEWRITER_SPEED, self.type_dialogue, text, index + 1, callback, sans_speaking)
        else:
            # typing is complete
            self.is_typing = False
            # trigger callback if provided (used for button state changes)
            if callback:
                callback()
    
    def stop_typing(self):
        """cancel all active typewriter animations and reset state"""
        # cancel scheduled dialogue animation
        if self.animation_text: 
            self.root.after_cancel(self.animation_text)
            self.animation_text = None
        # cancel scheduled Sans comment animation
        if self.animation_comment: 
            self.root.after_cancel(self.animation_comment)
            self.animation_comment = None
        # allow user interaction
        self.is_typing = False
    
    # === getting the jokes ===
    def load_jokes(self):
        """load all jokes from the jokes file"""
        jokes = []
        with open(JOKES_FILE_PATH, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # split setup and punchline by the question mark
                parts = line.split('?', 1)
                setup = parts[0].strip() + '?'  # keep question mark with setup
                punchline = parts[1].strip()
                jokes.append({'setup': setup, 'punchline': punchline})
        return jokes
    
    # === buttons ===
    def set_button(self, button, enabled):
        """enable or disable a button and update its visual state"""
        if button == self.btn_punchline:
            # track if punchline button is clickable
            self.button_enabled['punchline'] = enabled
            if enabled:
                # show colored image and bind click handler
                button.config(image=self.img_punchline)
                button.bind("<Button-1>", lambda e: self.show_punchline())
            else:
                # show grayscale image and remove click handler
                button.config(image=self.img_punchline_gray)
                button.unbind("<Button-1>")
        elif button == self.btn_next:
            # track if next button is clickable
            self.button_enabled['next'] = enabled
            if enabled:
                button.config(image=self.img_next)
                button.bind("<Button-1>", lambda e: self.next_joke())
            else:
                button.config(image=self.img_next_gray)
                button.unbind("<Button-1>")
        elif button == self.btn_tell:
            # tell joke button is always clickable when not typing
            if enabled:
                button.config(image=self.img_tell)
                button.bind("<Button-1>", lambda e: self.tell_joke())
            else:
                button.config(image=self.img_tell_gray)
                button.unbind("<Button-1>")
    
    # === music ===
    def play_music(self):
        """start background music on loop"""
        # load music file
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1) # -1 means infinite loop
        self.is_music_playing = True
        # show unmute icon to indicate music is playing
        self.btn_mute.config(image=self.img_mute)
    
    def toggle_music(self):
        """pause or resume music and update button visual"""
        if self.is_music_playing:
            # music is playing, so pause it
            pygame.mixer.music.pause()
            self.is_music_playing = False
            # show mute icon to indicate music is off
            self.btn_mute.config(image=self.img_unmute)
        else:
            # music is paused, so resume it
            pygame.mixer.music.unpause()
            self.is_music_playing = True
            # show unmute icon to indicate music is on
            self.btn_mute.config(image=self.img_mute)
    
    # === joke flow ===
    def tell_joke(self):
        """display joke setup and prepare for punchline"""
        # only allow new joke if not currently typing
        if not self.is_typing:
            # hide Sans comment box 
            self.text_sans.place_forget()
            # switch to setup GIF animation
            self.play_gif(self.gif_setup)
            
            # reposition dialogue box for better joke display
            self.label_dialogue.place(x=DIALOGUE_X + DIALOGUE_TEXT_X_OFFSET, y=DIALOGUE_Y + DIALOGUE_TEXT_Y_OFFSET, width=DIALOGUE_WIDTH - 40, height=DIALOGUE_TEXT_HEIGHT)
            self.label_dialogue.config(fg="#FFFFFF", bg=BG_COLOR, wraplength=DIALOGUE_WIDTH - 60)
            
            # randomly select a joke from loaded jokes
            self.current_joke = random.choice(self.jokes)
            
            # stop any previous animation
            self.stop_typing()
            self.is_typing = True
            # type setup with Sans speaking sounds, callback when done
            self.type_dialogue(self.current_joke['setup'], callback=self.on_setup_done, sans_speaking=True)
            
            # update button states - disable setup, enable next
            self.set_button(self.btn_punchline, False)
            self.set_button(self.btn_next, True)
            self.set_button(self.btn_tell, False)
    
root.mainloop()