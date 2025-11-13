from PIL import Image, ImageTk, ImageSequence


class GIFPlayer:
    """handles animated GIF playback on a label"""
    _all_gifs = []

    def __init__(self, label, gif_path, width, height):
        self.label = label
        self.frames = []
        self.current_frame = 0
        self.job = None

        # load and resize all GIF frames
        im = Image.open(gif_path)
        for frame in ImageSequence.Iterator(im):
            resized = frame.copy().resize((width, height), Image.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(resized))

        GIFPlayer._all_gifs.append(self)

    def play(self):
        """start playing the GIF"""
        self.stop()
        self.current_frame = 0
        self.animate()

    def animate(self):
        """show next frame"""
        if self.frames:
            self.label.config(image=self.frames[self.current_frame])
            self.label.image = self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.job = self.label.after(100, self.animate)

    def stop(self):
        """stop the animation"""
        if self.job:
            self.label.after_cancel(self.job)
            self.job = None

    @classmethod
    def stop_all(cls):
        """stop all GIF animations"""
        for gif in cls._all_gifs:
            gif.stop()