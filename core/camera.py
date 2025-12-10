class Camera:

    def __init__(self, x: float, y: float, scale: float):
        self.x: float = x  # Camera world position (X)
        self.y: float = y  # Camera world position (Y)
        self.scale: float = scale  # Zoom level
        self.velocity_x: float = 0.0  # Horizontal velocity for smooth camera movement
        self.velocity_y: float = 0.0  # Vertical velocity for smooth camera movement

    def project(self, x: float, y: float) -> tuple[float, float]:
        x = (x - self.x) * self.scale  # Translate and scale for horizontal
        y = (y - self.y) * self.scale  # Translate and scale for vertical
        return x, y

    def deduce(self, x: float, y: float) -> tuple[float, float]:
        x = x / self.scale + self.x  # Unscale and translate horizontal
        y = y / self.scale + self.y  # Unscale and translate vertical
        return x, y
