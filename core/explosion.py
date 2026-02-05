from core.asset import asset
from libraries.pgiud import Image, V

class Explosion:

    def __init__(self, x, y):
        self.pos = V(x, y)
        self.duration = 30
        self.frames = 10
        self.current_frame = 0
        self.scale = 1.0
        self.images = [Image(asset(f'images/explosion/explosion_{i}.png')) for i in range(self.frames)]

    def image(self):
        return self.images[self.current_frame]

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @x.setter
    def x(self, value):
        self.pos.x = float(value)

    @y.setter
    def y(self, value):
        self.pos.y = float(value)
