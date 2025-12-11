"""Game units and unit types for Fleet Command.

This module defines the Unit base class and specific unit types (e.g., Battleship).
Units represent the combat entities in the game with health, attack, defense, and movement.
"""

from panda2d import Image

class Unit:
    pass

    def __init__(
        self,
        image: Image,
        image_scale: float,
        health: int,
        speed: int,
        rotation_speed: int,
        friction: float = 0.95,
        rotation_friction: float = 0.9,
        collision_radius: int = 20
    ) -> None:
        # Appearance
        self.image = image  # Image used to render this unit
        self.image_scale = 1.0  # Scale applied to the image (independent of camera zoom)
        self.team_index = -1  # Index of the team this unit belongs to

        # Unit statistics
        self.max_health = health  # Maximum health/hit points
        self.health = health      # Current health/hit points

        # Position and direction
        self.position_x = 0  # X position on the game map
        self.position_y = 0  # Y position on the game map
        self.direction = 0   # Direction the unit is facing (degrees, 0=up)

        # Movement properties
        self.speed = speed  # Maximum linear movement speed
        self.rotation_speed = rotation_speed  # Maximum rotational speed (degrees/sec)

        self.velocity_x = 0  # Current velocity in X direction
        self.velocity_y = 0  # Current velocity in Y direction
        self.velocity_rotation = 0  # Current rotational velocity

        self.acceleration = 0  # Current acceleration for this frame
        self.rotation_acceleration = 0  # Current rotational acceleration for this frame

        self.friction = friction  # Friction factor applied each frame (slows movement)
        self.rotation_friction = rotation_friction  # Friction factor for rotation

        # Shooting/targeting
        self.gun_direction = 0  # Direction the unit's guns are facing (degrees)
        self.target_position_x = 0  # Target position for weapons (X coordinate)
        self.target_position_y = 0  # Target position for weapons (Y coordinate)

        # Collisions
        self.collision_radius = collision_radius  # Radius for collision detection

        # Autonomous control
        self.autonomous = False  # True if unit is controlled by autonomous movement
        self.autonomous_target_x = 0  # Target position for autonomous movement (X)
        self.autonomous_target_y = 0  # Target position for autonomous movement (Y)


class Battleship(Unit):
    def __init__(self, team_index, position_x=0, position_y=0, direction=0):
        # Initialize with battleship-specific stats
        super().__init__(
            Image("assets/images/battleship.png"),
            image_scale=0.1,
            health=600,  # High health
            speed=200,  # Fast movement speed
            rotation_speed=100,  # Rotation speed
            friction=0.97,  # Low friction (maintains momentum well)
            rotation_friction=0.9,  # Rotation friction
            collision_radius=30  # Larger collision radius
        )
        # Set initial position and team
        self.team_index = team_index
        self.position_x = position_x
        self.position_y = position_y
        self.direction = direction
