from core.asset import asset
from libraries.pgiud import Image


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.duration = 30
        self.frames = 10
        self.current_frame = 0
        self.scale = 1.0
        # Load images using the asset helper so paths are resolved relative to
        # src/
        self.images = [
            Image(asset(f"images/explosion_{i}.png")) for i in range(self.frames)
        ]

    def image(self):
        # The images list already contains Image instances — return the current
        # one
        return self.images[self.current_frame]
