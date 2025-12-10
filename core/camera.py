class Camera:
    """Simple camera for projecting between world and screen space."""

    def __init__(self, x: float, y: float, scale: float):
        self.x: float = x
        self.y: float = y
        self.scale: float = scale
        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0

    def project(self, x: float, y: float) -> tuple[float, float]:
        """Project world-space coordinates `(x, y)` to screen-space."""
        x = (x - self.x) * self.scale
        y = (y - self.y) * self.scale
        return x, y

    def deduce(self, x: float, y: float) -> tuple[float, float]:
        """Convert screen-space coordinates `(x, y)` to world-space."""
        x = x / self.scale + self.x
        y = y / self.scale + self.y
        return x, y
