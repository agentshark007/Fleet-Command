"""Team management and team color definitions for Fleet Command.

This module defines team types, team colors, and team classes that represent
player and AI-controlled factions in the game.
"""

from panda2d import Color
from enum import Enum
import random


class TeamType(Enum):
    """Enumeration for different team types.
    
    Distinguishes between player-controlled teams and AI-controlled teams.
    """
    PLAYER = "player"  # Team controlled by the player
    AI = "ai"          # Team controlled by AI

class TeamColor:
    """Represents a team color with associated display color.
    
    Base class for all team types, storing a team name and its associated
    Color object used for rendering team identifiers and UI elements.
    """

    def __init__(self, name: str, color: Color):
        """Initialize a team color.
        
        Args:
            name: Display name of the team.
            color: Color object used for rendering this team.
        """
        self.name = name  # Team display name
        self.color = color  # Team color for rendering


class Team:
    """Represents a team in the game.
    
    Stores team metadata including type (player or AI) and color.
    Units reference a team by its index in the game's team list.
    """

    def __init__(self, type: TeamType, color: TeamColor):
        """Initialize a team.
        
        Args:
            type: TeamType indicating if this is a player or AI team.
            color: TeamColor object defining the team's appearance.
        """
        self.type = type  # Team type (PLAYER or AI)
        self.color = color  # Team color for rendering


def random_teams(teams):
    """Generate a random selection of teams for a game.
    
    Creates a list of teams with one player-controlled team and the rest AI teams.
    Colors are selected randomly from available team colors. If more teams are requested
    than unique colors available, colors will be reused.
    
    Args:
        teams: Number of total teams to generate (must be >= 1).
        
    Returns:
        List of Team objects with the player team at index 0, followed by AI teams.
        Returns empty list if teams <= 0.
    """
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
    """Team with red color."""

    def __init__(self):
        """Initialize Red Fleet team with red color."""
        super().__init__("Red Fleet", Color(255, 0, 0))


class BlueAlliance(TeamColor):
    """Team with blue color."""

    def __init__(self):
        """Initialize Blue Alliance team with blue color."""
        super().__init__("Blue Alliance", Color(0, 0, 255))


class GreenSquadron(TeamColor):
    """Team with green color."""

    def __init__(self):
        """Initialize Green Squadron team with green color."""
        super().__init__("Green Squadron", Color(0, 255, 0))


class YellowLegion(TeamColor):
    """Team with yellow color."""

    def __init__(self):
        """Initialize Yellow Legion team with yellow color."""
        super().__init__("Yellow Legion", Color(255, 255, 0))


class PurpleVanguard(TeamColor):
    """Team with purple color."""

    def __init__(self):
        """Initialize Purple Vanguard team with purple color."""
        super().__init__("Purple Vanguard", Color(128, 0, 128))


class OrangeCrew(TeamColor):
    """Team with orange color."""

    def __init__(self):
        """Initialize Orange Crew team with orange color."""
        super().__init__("Orange Crew", Color(255, 165, 0))


class CyanForce(TeamColor):
    """Team with cyan color."""

    def __init__(self):
        """Initialize Cyan Force team with cyan color."""
        super().__init__("Cyan Force", Color(0, 255, 255))