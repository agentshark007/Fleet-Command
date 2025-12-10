"""Game units and unit types for Fleet Command.

This module defines the Unit base class and specific unit types (e.g., Battleship).
Units represent the combat entities in the game with health, attack, defense, and movement.
"""

from panda2d import Image

class Unit:
    """Base class for all game units.
    
    Represents a game entity with appearance, statistics, position, velocity,
    and control properties for both player and autonomous movement.
    """

    def __init__(
        self, image: Image, image_scale: float, health: int, attack: int, defense: int,
        speed: int, rotation_speed: int, friction: float = 0.95, rotation_friction: float = 0.9
    ):
        """Initialize a unit with the given stats and properties.
        
        Args:
            image: Panda2D Image object for rendering this unit.
            image_scale: Scale factor for displaying the unit image.
            health: Hit points of the unit.
            attack: Attack power of the unit.
            defense: Defensive rating of the unit.
            speed: Maximum movement speed.
            rotation_speed: Maximum rotation speed (degrees per second).
            friction: Friction factor for movement decay (0-1).
            rotation_friction: Friction factor for rotation decay (0-1).
        """
        # Appearance
        self.image = image  # Image used to render this unit
        self.image_scale = 1.0  # Scale applied to the image (independent of camera zoom)
        self.team_index = -1  # Index of the team this unit belongs to

        # Unit statistics
        self.health = health  # Current health/hit points
        self.attack = attack  # Attack damage value
        self.defense = defense  # Defensive rating

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

        # Autonomous control
        self.autonomous = False  # True if unit is controlled by autonomous movement
        self.autonomous_target_x = 0  # Target position for autonomous movement (X)
        self.autonomous_target_y = 0  # Target position for autonomous movement (Y)


class Battleship(Unit):
    """A heavy combat unit with high health and damage.
    
    Battleships are slow-moving but heavily armored units with high attack power.
    They are the primary combat units in Fleet Command.
    """

    def __init__(self, team_index, position_x=0, position_y=0, direction=0):
        """Initialize a Battleship unit.
        
        Args:
            team_index: Index of the team this battleship belongs to.
            position_x: Starting X position on the map (default: 0).
            position_y: Starting Y position on the map (default: 0).
            direction: Starting direction facing (degrees, default: 0).
        """
        # Initialize with battleship-specific stats
        super().__init__(
            Image("assets/images/battleship.png"),
            image_scale=0.1,
            health=600,  # High health
            attack=150,  # High attack power
            defense=100,  # Strong defense
            speed=200,  # Fast movement speed
            rotation_speed=100,  # Rotation speed
            friction=0.97,  # Low friction (maintains momentum well)
            rotation_friction=0.9  # Rotation friction
        )
        # Set initial position and team
        self.team_index = team_index
        self.position_x = position_x
        self.position_y = position_y
        self.direction = direction
