from core.asset import asset
from libraries.pgiud import Image, V


class Unit:
    pass

    def __init__(self, image: Image, image_scale: float, health: int, speed: int, rotation_speed: int, friction: float = 0.95, rotation_friction: float = 0.9, collision_radius: int = 20) -> None:
        self.image = image
        self.image_scale = 1.0
        self.team_index = -1
        self.max_health = health
        self.health = health
        self.position = V(0, 0)
        self.direction = 0
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.velocity = V(0, 0)
        self.velocity_rotation = 0
        self.acceleration = 0
        self.rotation_acceleration = 0
        self.friction = friction
        self.rotation_friction = rotation_friction
        self.gun_direction = 0
        self.target_position = V(0, 0)
        self.collision_radius = collision_radius
        self.autonomous = False
        self.autonomous_target = V(0, 0)
        self.ai_wander_target = V(0, 0)
        self.cooldown_timer = 0

    @property
    def position_x(self) -> float:
        return self.position.x

    @position_x.setter
    def position_x(self, value: float) -> None:
        self.position.x = float(value)

    @property
    def position_y(self) -> float:
        return self.position.y

    @position_y.setter
    def position_y(self, value: float) -> None:
        self.position.y = float(value)

    @property
    def velocity_x(self) -> float:
        return self.velocity.x

    @velocity_x.setter
    def velocity_x(self, value: float) -> None:
        self.velocity.x = float(value)

    @property
    def velocity_y(self) -> float:
        return self.velocity.y

    @velocity_y.setter
    def velocity_y(self, value: float) -> None:
        self.velocity.y = float(value)

    @property
    def target_position_x(self) -> float:
        return self.target_position.x

    @target_position_x.setter
    def target_position_x(self, value: float) -> None:
        self.target_position.x = float(value)

    @property
    def target_position_y(self) -> float:
        return self.target_position.y

    @target_position_y.setter
    def target_position_y(self, value: float) -> None:
        self.target_position.y = float(value)

    @property
    def autonomous_target_x(self) -> float:
        return self.autonomous_target.x

    @autonomous_target_x.setter
    def autonomous_target_x(self, value: float) -> None:
        self.autonomous_target.x = float(value)

    @property
    def autonomous_target_y(self) -> float:
        return self.autonomous_target.y

    @autonomous_target_y.setter
    def autonomous_target_y(self, value: float) -> None:
        self.autonomous_target.y = float(value)

    @property
    def ai_wander_target_x(self) -> float:
        return self.ai_wander_target.x

    @ai_wander_target_x.setter
    def ai_wander_target_x(self, value: float) -> None:
        self.ai_wander_target.x = float(value)

    @property
    def ai_wander_target_y(self) -> float:
        return self.ai_wander_target.y

    @ai_wander_target_y.setter
    def ai_wander_target_y(self, value: float) -> None:
        self.ai_wander_target.y = float(value)


class Battleship(Unit):

    def __init__(self, team_index, position_x=0, position_y=0, direction=0):
        super().__init__(Image(asset('images/units/battleship.png')), image_scale=0.1, health=600,
                         speed=200, rotation_speed=100, friction=0.97, rotation_friction=0.9, collision_radius=25)
        self.team_index = team_index
        self.position = V(position_x, position_y)
        self.direction = direction


class Warship(Unit):

    def __init__(self, team_index, position_x=0, position_y=0, direction=0):
        super().__init__(Image(asset('images/units/warship.png')), image_scale=0.1, health=400,
                         speed=250, rotation_speed=150, friction=0.95, rotation_friction=0.85, collision_radius=25)
        self.team_index = team_index
        self.position = V(position_x, position_y)
        self.direction = direction
