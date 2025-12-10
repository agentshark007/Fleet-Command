import math

def calculate_direction(target_x, target_y):
    """Calculate the direction vector towards the target coordinates."""
    length = math.sqrt(target_x**2 + target_y**2)
    if length == 0:
        return 0, 0
    return target_x / length, target_y / length

class Projectile:
    """Class representing a projectile in the game."""
    
    def __init__(self, x, y, target_x, target_y, speed, shooter_index):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = calculate_direction(target_x, target_y)
        self.visible_direction = math.atan2(self.direction[1], self.direction[0])
        self.damage = 10
        self.shooter_index = shooter_index # Here to prevent self-hits
    
    def update(self, deltatime):
        """Update the projectile's position based on its speed and direction."""
        self.x += self.direction[0] * self.speed * deltatime
        self.y += self.direction[1] * self.speed * deltatime

class Missile(Projectile):
    """Class representing a missile projectile."""
    
    def __init__(self, x, y, target_x, target_y, shooter_index):
        super().__init__(x, y, target_x, target_y, speed=7, shooter_index=shooter_index)
        self.damage = 20
