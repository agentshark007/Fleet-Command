

from panda2d import Color
from enum import Enum
import random


class TeamType(Enum):
    pass
    PLAYER = "player"  # Team controlled by the player
    AI = "ai"          # Team controlled by AI

class TeamColor:
    pass

    def __init__(self, name: str, color: Color) -> None:
        pass
        self.name = name  # Team display name
        self.color = color  # Team color for rendering


class Team:
    pass

    def __init__(self, type: TeamType, color: TeamColor) -> None:
        pass
        self.type = type  # Team type (PLAYER or AI)
        self.color = color  # Team color for rendering


def random_teams(teams: int) -> list[Team]:
    pass
    # Define all available team colors
    all_team_colors = [
        RedFleet(),
        BlueAlliance(),
        GreenSquadron(),
        YellowLegion(),
        PurpleVanguard(),
        OrangeCrew(),
        CyanForce()
    ]

    # Defensive: non-positive team counts -> return empty list
    if teams <= 0:
        return []

    # If we have enough distinct colors, pick without replacement so colors
    # won't repeat. Otherwise allow repeats to reach the requested count.
    available_count = len(all_team_colors)

    if teams <= available_count:
        # Pick unique colors for the requested number of teams
        chosen = random.sample(all_team_colors, teams)
        # Select a random color for the player and make the rest AI teams
        player_color = random.choice(chosen)
        ai_colors = [c for c in chosen if c is not player_color]
        # Create AI teams first, then insert player team at index 0
        selected_teams = [Team(TeamType.AI, color) for color in ai_colors]
        selected_teams.insert(0, Team(TeamType.PLAYER, player_color))
        return selected_teams
    else:
        # Not enough unique colors: include one of each color first, then
        # fill remaining AI slots with random choices (duplicates allowed)
        selected_teams = [Team(TeamType.AI, color) for color in all_team_colors]
        # Calculate how many extra teams are needed beyond the unique colors
        extra_needed = teams - 1 - available_count
        if extra_needed > 0:
            # Add additional AI teams with random colors (may repeat)
            for color in random.choices(all_team_colors, k=extra_needed):
                selected_teams.append(Team(TeamType.AI, color))

        # Select a random color for the player team
        player_color = random.choice(all_team_colors)
        selected_teams.insert(0, Team(TeamType.PLAYER, player_color))
        return selected_teams



class RedFleet(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Red Fleet", Color(255, 0, 0))


class BlueAlliance(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Blue Alliance", Color(0, 0, 255))


class GreenSquadron(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Green Squadron", Color(0, 255, 0))


class YellowLegion(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Yellow Legion", Color(255, 255, 0))


class PurpleVanguard(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Purple Vanguard", Color(128, 0, 128))


class OrangeCrew(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Orange Crew", Color(255, 165, 0))


class CyanForce(TeamColor):
    pass

    def __init__(self):
        pass
        super().__init__("Cyan Force", Color(0, 255, 255))