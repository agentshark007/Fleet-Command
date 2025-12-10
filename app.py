from panda2d import PandaWindow, Color, Font, Image, Sound, Key, Anchor, Resizable
import math
from game.team import *
from game.unit import *
from core.utility import distance, mouse_in_area
from enum import Enum
import random
from core.camera import Camera
from core.enums import ExtendDirection, GameState
from iud import core
from iud import game
from iud import mainmenu
from iud import newgame
from iud import paused
from iud import settings


# Game window
class GameWindow(PandaWindow):
    def __init__(self):
        super().__init__(
            width=800,
            height=600,
            title="Fleet Command",
            resizable=Resizable.BOTH,
            anchor=Anchor.CENTER
        )

    def extend(self, pivot, value, direction: ExtendDirection):
        return pivot + (value * direction.value * self.gui_scale)


    def initialize(self):
        core.initialize(self)
        game.initialize(self)
        mainmenu.initialize(self)
        newgame.initialize(self)
        paused.initialize(self)
        settings.initialize(self)


    def update(self):
        core.update(self)

        match self.game_state:
            case GameState.MAINMENU:
                mainmenu.update(self)
            case GameState.NEWGAME:
                newgame.update(self)
            case GameState.GAME:
                game.update(self)
            case GameState.PAUSED:
                paused.update(self)
            case GameState.SETTINGS:
                settings.update(self)

        core.late_update(self)


    def draw(self):
        """Main per-frame draw: renders current state to the screen."""
        core.draw(self)

        match self.game_state:
            case GameState.MAINMENU:
                mainmenu.draw(self)
            case GameState.NEWGAME:
                newgame.draw(self)
            case GameState.GAME:
                game.draw(self)
            case GameState.PAUSED:
                paused.draw(self)
            case GameState.SETTINGS:
                settings.draw(self)



def main():
    window = GameWindow()
    window.start()
