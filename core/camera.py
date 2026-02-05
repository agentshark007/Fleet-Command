from libraries.pgiud import V

class Camera:

    def __init__(self, x: float, y: float, scale: float):
        self.pos: V = V(x, y)
        self.scale: float = scale
        self.velocity: V = V(0.0, 0.0)

    @property
    def x(self) -> float:
        return self.pos.x

    @x.setter
    def x(self, value: float) -> None:
        self.pos.x = float(value)

    @property
    def y(self) -> float:
        return self.pos.y

    @y.setter
    def y(self, value: float) -> None:
        self.pos.y = float(value)

    @property
    def velocity_x(self) -> float:
        return self.velocity.x

    @velocity_x.setter
    def velocity_x(self, value: float) -> None:
        self.velocity.x = float(value)

    @property
    def velocity_y(self) -> float:
        return self.velocity.y

    @velocity_y.setter
    def velocity_y(self, value: float) -> None:
        self.velocity.y = float(value)

    def project(self, x: float, y: float) -> tuple[float, float]:
        x = (x - self.x) * self.scale
        y = (y - self.y) * self.scale
        return (x, y)

    def deduce(self, x: float, y: float) -> tuple[float, float]:
        x = x / self.scale + self.x
        y = y / self.scale + self.y
        return (x, y)

    def project_v(self, v: V) -> V:
        px, py = self.project(v.x, v.y)
        return V(px, py)

    def deduce_v(self, v: V) -> V:
        dx, dy = self.deduce(v.x, v.y)
        return V(dx, dy)
