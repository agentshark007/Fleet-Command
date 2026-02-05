import math
import random
from libraries.pgiud import V


def calculate_direction(
    origin_x: float, origin_y: float, target_x: float, target_y: float
) -> float:
    dx = target_x - origin_x
    dy = target_y - origin_y
    angle_rad = math.atan2(dy, dx)
    return math.degrees(angle_rad)


class Projectile:

    def __init__(
        self,
        x: float,
        y: float,
        direction: float,
        shooter_id: int,
        speed: float,
        damage: int,
        cooldown: float,
        fuel: float,
        accuracy: float,
    ) -> None:
        self.pos = V(x, y)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.shooter_id = shooter_id
        self.cooldown = cooldown
        self.fuel = fuel
        self.accuracy = accuracy

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

    def update(self, deltatime: float) -> None:
        self.direction += math.sin(self.x * self.y) * self.accuracy * deltatime
        rad = math.radians(self.direction)
        self.pos.x += math.cos(rad) * self.speed * deltatime
        self.pos.y += math.sin(rad) * self.speed * deltatime

    def update_fuel(self, deltatime: float) -> None:
        self.fuel -= deltatime


class Missile(Projectile):

    def __init__(self, x: float, y: float, direction: float, shooter_id: int) -> None:
        super().__init__(
            x,
            y,
            direction,
            shooter_id=shooter_id,
            speed=100,
            damage=2,
            cooldown=0.5,
            fuel=15,
            accuracy=5,
        )
