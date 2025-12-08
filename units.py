from panda2d import Image

class Unit:
    """Represents a unit in the game."""

    def __init__(
        self, image: Image, health: int, attack: int, defense: int,
        speed: int, rotation_speed: int, friction: float = 0.95, rotation_friction: float = 0.9
    ):
        # Apperance
        self.image = image
        self.scale = 1.0
        self.team = None  # Assigned team

        # Stats
        self.health = health
        self.attack = attack
        self.defense = defense

        # Position
        self.position_x = 0  # X position on the map
        self.position_y = 0  # Y position on the map
        self.direction = 0   # Direction the unit is facing (degrees)

        # Speed, velocity, and friction
        self.speed = speed
        self.rotation_speed = rotation_speed

        self.velocity_x = 0  # Velocity in the X direction
        self.velocity_y = 0  # Velocity in the Y direction
        self.velocity_rotation = 0  # Rotational velocity

        self.friction = friction  # Friction factor for movement
        self.rotation_friction = rotation_friction  # Friction factor for rotation

        # Shooting
        self.gun_direction = 0  # Direction the unit's gun is facing (degrees)
        self.target_position_x = 0  # Target position for shooting (X coordinate)
        self.target_position_y = 0  # Target position for shooting (Y coordinate)

        # Autonomous control
        self.autonomous = False  # Whether the unit is controlled autonomously
        self.autonomous_target_x = 0  # Autonomous target position X
        self.autonomous_target_y = 0  # Autonomous target position Y


class Battleship(Unit):
    """Represents a Battleship unit."""

    def __init__(self, team, position_x=0, position_y=0, direction=0):
        super().__init__(
            Image("assets/images/battleship.png"),
            health=600,
            attack=150,
            defense=100,
            speed=100,
            rotation_speed=100,
            friction=0.97,
            rotation_friction=0.9
        )
        self.team = team
        self.position_x = position_x
        self.position_y = position_y
        self.target_position_x = position_x
        self.target_position_y = position_y
        self.direction = direction
