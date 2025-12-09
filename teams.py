from panda2d import Color
from enum import Enum

class TeamType(Enum):
    """Enumeration for different team types."""
    PLAYER = "player"
    AI = "ai"


class Team:
    """Represents a team in the game."""

    def __init__(self, name: str, color: Color, type: TeamType):
        self.name = name
        self.color = color
        self.type = type


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


class YellowLegion(Team):
    """Represents the Yellow Legion team."""

    def __init__(self):
        super().__init__("Yellow Legion", Color(255, 255, 0))


class PurpleVanguard(Team):
    """Represents the Purple Vanguard team."""

    def __init__(self):
        super().__init__("Purple Vanguard", Color(128, 0, 128))


class OrangeCrew(Team):
    """Represents the Orange Crew team."""

    def __init__(self):
        super().__init__("Orange Crew", Color(255, 165, 0))


class CyanForce(Team):
    """Represents the Cyan Force team."""

    def __init__(self):
        super().__init__("Cyan Force", Color(0, 255, 255))