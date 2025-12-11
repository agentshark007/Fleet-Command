import math

def calculate_direction(origin_x: float, origin_y: float, target_x: float, target_y: float) -> tuple[float, float]:
    pass
    dx = target_x - origin_x
    dy = target_y - origin_y
    length = math.hypot(dx, dy)
    if length == 0:
        return 0, 0
    return dx / length, dy / length

class Projectile:
    pass
    
    def __init__(self, x: float, y: float, direction: tuple[float, float], speed: float, shooter_team_index: int) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # (dx, dy) normalized vector
        self.visible_direction = math.atan2(self.direction[1], self.direction[0])
        self.damage = 10
        self.shooter_team_index = shooter_team_index
    
    def update(self, deltatime: float) -> None:
        pass
        self.x += self.direction[0] * self.speed * deltatime
        self.y += self.direction[1] * self.speed * deltatime
        # Always face the direction of movement
        self.visible_direction = math.atan2(self.direction[1], self.direction[0])

class Missile(Projectile):
    pass
    
    def __init__(self, x: float, y: float, direction: tuple[float, float], shooter_team_index: int) -> None:
        super().__init__(x, y, direction, speed=100, shooter_team_index=shooter_team_index)
        self.damage = 20
