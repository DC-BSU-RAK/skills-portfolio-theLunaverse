from PIL import Image, ImageTk, ImageSequence
import tkinter as tk

from modules.constants import *


class GIFPlayer:
    """Handles animated GIF playback on a label"""
    # track all GIF instances in the application
    _all_gifs = []

    def __init__(self, label, gif_path, width, height):
        self.label = label  # where the GIF will be shown
        self.frames = []  # store all frames of the GIF
        self.current_frame = 0
        self.job = None  # in order to stop the animation later

        # open the GIF file
        im = Image.open(gif_path)
        for frame in ImageSequence.Iterator(im):  # go through each frame in GIF
            resized = frame.copy().resize((width, height), Image.LANCZOS)  # LANCZOS from pillow for best quality
            self.frames.append(ImageTk.PhotoImage(resized))  # resized the frame and convert it so Tkinter can show it

        # add this GIF to the list of all GIFs
        GIFPlayer._all_gifs.append(self)

    def play(self):
        """Start playing the GIF from the beginning"""
        self.stop()
        self.current_frame = 0
        self.animate()  # begin loop

    def animate(self):
        """Show next frame"""
        if self.frames:
            self.label.config(image=self.frames[self.current_frame])  # update the label image
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

    @classmethod
    def stop_all(cls):
        """Stop all GIF animations in the application"""
        for gif in cls._all_gifs:
            gif.stop()


class QuizFrame:
    """Manages background GIF for each difficulty level"""
    # cache to store already created frames (so we don't recreate them)
    _cache = {}

    def __init__(self, parent, diff):
        # create a label to hold background GIF
        self.bg = tk.Label(parent)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # store the background color for labels in this difficulty
        self.label_bg = diff.color
        
        # create the GIF player for this difficulty's background
        self.gif = GIFPlayer(self.bg, diff.path, WINDOW_WIDTH, WINDOW_HEIGHT)

    @classmethod
    def get_or_create(cls, parent, diff):
        """Get existing frame from cache or create new one if it doesn't exist"""
        if diff not in cls._cache:
            cls._cache[diff] = cls(parent, diff)
        return cls._cache[diff]

    def play(self):
        """Start playing this frame's background GIF"""
        self.gif.play()

    def stop(self):
        """Stop playing this frame's background GIF"""
        self.gif.stop()

    def start(self):
        """Bring this frame to front and start playing its GIF"""
        self.bg.tkraise()
        self.play()