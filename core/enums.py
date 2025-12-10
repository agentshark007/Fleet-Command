"""Enumeration types used throughout the Fleet Command game.

This module defines enums for game state management and UI layout directions.
"""

from enum import Enum

class ExtendDirection(Enum):
    """Direction values for extending UI positions.
    
    Used in the GameWindow.extend() method to calculate scaled position offsets.
    Values are multiplied with distance and GUI scale to determine final positions.
    """
    LEFT = -1   # Used for horizontal extension (moves left)
    RIGHT = 1   # Used for horizontal extension (moves right)
    UP = 1      # Used for vertical extension (moves up)
    DOWN = -1   # Used for vertical extension (moves down)

class GameState(Enum):
    """Enumeration of all possible game states.
    
    Used to manage the current screen/mode the game is in and route
    update and draw calls to the appropriate handler.
    """
    MAINMENU = "mainmenu"  # Main menu screen
    NEWGAME = "newgame"    # New game setup screen
    GAME = "game"          # Active gameplay
    PAUSED = "paused"      # Game paused
    SETTINGS = "settings"  # Settings menu
    