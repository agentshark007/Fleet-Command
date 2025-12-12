from panda2d import Image


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.duration = 30
        self.frames = 10
        self.current_frame = 0
        self.image_prefix = "assets/images/explosion_"
        self.image_suffix = ".png"
        self.scale = 1.0
        self.images = [
            Image(f"{self.image_prefix}{i}{self.image_suffix}")
            for i in range(self.frames)
        ]

    def image(self):
        # The images list already contains Image instances — return the current one
        return self.images[self.current_frame]
