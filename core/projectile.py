import math


def calculate_direction(
    origin_x: float, origin_y: float, target_x: float, target_y: float
) -> float:
    dx = target_x - origin_x
    dy = target_y - origin_y
    angle_rad = math.atan2(dy, dx)
    return math.degrees(angle_rad)


class Projectile:
    def __init__(self, x: float, y: float, direction: float, shooter_id: int, speed: float, damage: int, cooldown: float) -> None:
        self.x = x
        self.y = y
        self.direction = direction  # degrees
        self.speed = speed
        self.damage = damage
        self.shooter_id = shooter_id

    def update(self, deltatime: float) -> None:
        rad = math.radians(self.direction)
        self.x += math.cos(rad) * self.speed * deltatime
        self.y += math.sin(rad) * self.speed * deltatime


class Missile(Projectile):
    def __init__(self, x: float, y: float, direction: float, shooter_id: int) -> None:
        super().__init__(x, y, direction, shooter_id=shooter_id, speed=100, damage=2, cooldown=0.5)
