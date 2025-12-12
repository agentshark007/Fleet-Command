from panda2d import Color
from enum import Enum
import random


class TeamType(Enum):
    PLAYER = "player"  # Team controlled by the player
    AI = "ai"          # Team controlled by AI

class TeamColor:
    def __init__(self, name: str, color: Color) -> None:
        self.name = name  # Team display name
        self.color = color  # Team color for rendering


class Team:
    def __init__(self, type: TeamType, name: str, color: Color) -> None:
        self.type = type  # Team type (PLAYER or AI)
        self.name = name  # Team display name
        self.color = color  # Team color for rendering


def random_teams(teams: int) -> list[Team]:
    remaining_colors = team_colors.copy()
    random.shuffle(remaining_colors)

    result = []
    for i in range(teams):
        if remaining_colors:
            team_color = remaining_colors.pop(0)
            name = team_color.name
            color = team_color.color
        else:
            team_color = random.choice(team_colors)
            name = team_color.name
            color = team_color.color

        if i == 0:
            result.append(Team(TeamType.PLAYER, name, color))
        else:
            result.append(Team(TeamType.AI, name, color))
    return result

team_colors = [
    TeamColor("Red Fleet", Color(255, 0, 0)),
    TeamColor("Blue Alliance", Color(0, 0, 255)),
    TeamColor("Green Squadron", Color(0, 255, 0)),
    TeamColor("Yellow Legion", Color(255, 255, 0)),
    TeamColor("Purple Vanguard", Color(128, 0, 128)),
    TeamColor("Orange Crew", Color(255, 165, 0)),
    TeamColor("Cyan Force", Color(0, 255, 255)),
]
