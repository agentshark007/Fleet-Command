from panda2d import Color

class Team:
    """Represents a team in the game."""

    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color


class RedFleet(Team):
    """Represents the Red Fleet team."""

    def __init__(self):
        super().__init__("Red Fleet", Color(255, 0, 0))


class BlueAlliance(Team):
    """Represents the Blue Alliance team."""

    def __init__(self):
        super().__init__("Blue Alliance", Color(0, 0, 255))


class GreenSquadron(Team):
    """Represents the Green Squadron team."""

    def __init__(self):
        super().__init__("Green Squadron", Color(0, 255, 0))