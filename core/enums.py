

from enum import Enum


class ExtendDirection(Enum):
    LEFT = -1   # Used for horizontal extension (moves left)
    RIGHT = 1   # Used for horizontal extension (moves right)
    UP = 1      # Used for vertical extension (moves up)
    DOWN = -1   # Used for vertical extension (moves down)


class GameState(Enum):
    MAINMENU = "mainmenu"  # Main menu screen
    NEWGAME = "newgame"    # New game setup screen
    GAME = "game"          # Active gameplay
    PAUSED = "paused"      # Game paused
    SETTINGS = "settings"  # Settings menu
