from panda2d import Color
from enum import Enum
import random



class TeamType(Enum):
    """Enumeration for different team types."""
    PLAYER = "player"
    AI = "ai"

class TeamColor:
    """Represents a team color in the game."""

    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color


class Team:
    """Stores information about a team in the game. Units are stored in a unit list elsewhere and are referencing a team by team index in a team list."""

    def __init__(self, type: TeamType, color: TeamColor):
        self.type = type
        self.color = color


def random_teams(teams):
    """Returns a random selection of AI teams with one Player team with random color.

    No teams will be picked twice unless `teams` is greater than the number of
    available colors. The returned list always contains the Player team at index
    0 and the remaining entries are AI teams.
    """
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
        # Pick `teams` unique colors.
        chosen = random.sample(all_team_colors, teams)
        # Choose a player color from the chosen set and make the rest AI.
        player_color = random.choice(chosen)
        ai_colors = [c for c in chosen if c is not player_color]
        selected_teams = [Team(TeamType.AI, color) for color in ai_colors]
        selected_teams.insert(0, Team(TeamType.PLAYER, player_color))
        return selected_teams
    else:
        # Not enough unique colors: include one of each color first, then
        # fill remaining AI slots with random choices (duplicates allowed).
        selected_teams = [Team(TeamType.AI, color) for color in all_team_colors]
        extra_needed = teams - 1 - available_count
        if extra_needed > 0:
            for color in random.choices(all_team_colors, k=extra_needed):
                selected_teams.append(Team(TeamType.AI, color))

        # Player color can be any of the available colors.
        player_color = random.choice(all_team_colors)
        selected_teams.insert(0, Team(TeamType.PLAYER, player_color))
        return selected_teams



class RedFleet(TeamColor):
    """Represents the Red Fleet team."""

    def __init__(self):
        super().__init__("Red Fleet", Color(255, 0, 0))


class BlueAlliance(TeamColor):
    """Represents the Blue Alliance team."""

    def __init__(self):
        super().__init__("Blue Alliance", Color(0, 0, 255))


class GreenSquadron(TeamColor):
    """Represents the Green Squadron team."""

    def __init__(self):
        super().__init__("Green Squadron", Color(0, 255, 0))


class YellowLegion(TeamColor):
    """Represents the Yellow Legion team."""

    def __init__(self):
        super().__init__("Yellow Legion", Color(255, 255, 0))


class PurpleVanguard(TeamColor):
    """Represents the Purple Vanguard team."""

    def __init__(self):
        super().__init__("Purple Vanguard", Color(128, 0, 128))


class OrangeCrew(TeamColor):
    """Represents the Orange Crew team."""

    def __init__(self):
        super().__init__("Orange Crew", Color(255, 165, 0))


class CyanForce(TeamColor):
    """Represents the Cyan Force team."""

    def __init__(self):
        super().__init__("Cyan Force", Color(0, 255, 255))