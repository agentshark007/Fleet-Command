from enum import Enum

class ExtendDirection(Enum):
    LEFT = -1   # Used for horizontal extension
    RIGHT = 1   # Used for horizontal extension
    UP = 1      # Used for vertical extension
    DOWN = -1   # Used for vertical extension


class GameState(Enum):
    MAINMENU = "mainmenu"
    NEWGAME = "newgame"
    GAME = "game"
    PAUSED = "paused"
    SETTINGS = "settings"
    