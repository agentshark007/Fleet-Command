from panda2d import PandaWindow, Anchor, Resizable
from game.team import *
from game.unit import *
from core.enums import ExtendDirection, GameState
from iud import core
from iud import game
from iud import mainmenu
from iud import newgame
from iud import paused
from iud import settings


class GameWindow(PandaWindow):

    def __init__(self) -> None:
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
        self.menu_state = GameState.MAINMENU # Current game state tracking

        core.initialize(self)  # Initialize core systems (assets, GUI scale)

        game.initialize(self)  # Initialize gameplay systems
        mainmenu.initialize(self)  # Initialize main menu UI
        newgame.initialize(self)  # Initialize new game screen
        paused.initialize(self)  # Initialize pause menu
        settings.initialize(self)  # Initialize settings menu

        core.late_initialize(self)  # Finalize core systems if needed


    def update(self):
        core.update(self)  # Update core systems (GUI scaling)

        # Route update to current game state
        match self.menu_state:
            case GameState.MAINMENU:
                mainmenu.update(self)
            case GameState.NEWGAME:
                newgame.update(self)
            case GameState.GAME:
                game.update(self)  # Main gameplay loop
            case GameState.PAUSED:
                paused.update(self)
            case GameState.SETTINGS:
                settings.update(self)

        core.late_update(self)  # Finalize core systems (update key state for next frame)


    def draw(self):
        core.draw(self)  # Draw core systems if needed

        # Route drawing to current game state
        match self.menu_state:
            case GameState.MAINMENU:
                mainmenu.draw(self)
            case GameState.NEWGAME:
                newgame.draw(self)
            case GameState.GAME:
                game.draw(self)  # Draw game world, units, and UI
            case GameState.PAUSED:
                paused.draw(self)
            case GameState.SETTINGS:
                settings.draw(self)

        core.late_draw(self)  # Finalize core drawing if needed


def main():
    window = GameWindow()
    window.start()  # Start the main game loop
