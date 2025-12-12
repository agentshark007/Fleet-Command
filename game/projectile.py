import math

def calculate_direction(origin_x: float, origin_y: float, target_x: float, target_y: float) -> float:
    dx = target_x - origin_x
    dy = target_y - origin_y
    angle_rad = math.atan2(dy, dx)
    return math.degrees(angle_rad)

class Projectile:
    def __init__(self, x: float, y: float, direction: float, speed: float, shooter_id: int) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # angle in degrees
        self.damage = 10
        self.shooter_id = shooter_id

    def update(self, deltatime: float) -> None:
        rad = math.radians(self.direction)
        self.x += math.cos(rad) * self.speed * deltatime
        self.y += math.sin(rad) * self.speed * deltatime

class Missile(Projectile):
    def __init__(self, x: float, y: float, direction: float, shooter_id: int) -> None:
        super().__init__(x, y, direction, speed=100, shooter_id=shooter_id)
        self.damage = 20
