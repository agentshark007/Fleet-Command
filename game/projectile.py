import math

def calculate_direction(origin_x, origin_y, target_x, target_y):
    """Calculate the normalized direction vector from origin to target."""
    dx = target_x - origin_x
    dy = target_y - origin_y
    length = math.hypot(dx, dy)
    if length == 0:
        return 0, 0
    return dx / length, dy / length

class Projectile:
    """Class representing a projectile in the game."""
    
    def __init__(self, x, y, direction, speed, shooter_id):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # (dx, dy) normalized vector
        self.visible_direction = math.atan2(self.direction[1], self.direction[0])
        self.damage = 10
        self.shooter_id = shooter_id # Use unique unit_id for shooter
    
    def update(self, deltatime):
        """Update the projectile's position based on its speed and direction."""
        self.x += self.direction[0] * self.speed * deltatime
        self.y += self.direction[1] * self.speed * deltatime
        # Always face the direction of movement
        self.visible_direction = math.atan2(self.direction[1], self.direction[0])

class Missile(Projectile):
    """Class representing a missile projectile."""
    
    def __init__(self, x, y, direction, shooter_id):
        super().__init__(x, y, direction, speed=100, shooter_id=shooter_id)
        self.damage = 20
