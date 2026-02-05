from enum import Enum

class ExtendDirection(Enum):
    LEFT = -1
    RIGHT = 1
    UP = 1
    DOWN = -1

class GameState(Enum):
    MAINMENU = 'mainmenu'
    NEWGAME = 'newgame'
    GAME = 'game'
    PAUSED = 'paused'
    SETTINGS = 'settings'
