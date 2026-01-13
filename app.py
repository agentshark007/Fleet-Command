from core.enums import ExtendDirection, GameState
from iud import core, game, mainmenu, newgame, paused, settings
from pgiud import *
import log


class GameWindow(Window):
    def __init__(self) -> None:
        super().__init__(
            width=800,
            height=600,
            title="Fleet Command",
            resizable=Resizable.BOTH,
            origin=Origin.CENTER,
        )

    def extend(self, pivot, value, direction: ExtendDirection):
        return pivot + (value * direction.value * self.gui_scale)

    def initialize(self):
        log.info("Global initialization started")
        self.menu_state = GameState.MAINMENU  # Current game state tracking

        core.initialize(self)  # Initialize core systems (assets, GUI scale)

        game.initialize(self)  # Initialize gameplay systems
        mainmenu.initialize(self)  # Initialize main menu UI
        newgame.initialize(self)  # Initialize new game screen
        paused.initialize(self)  # Initialize pause menu
        settings.initialize(self)  # Initialize settings menu

        core.late_initialize(self)  # Finalize core systems if needed
        log.info("Global initialization complete")

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

        # Finalize core systems (update key state for next frame)
        core.late_update(self)

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
    log.reset("fleet-command.log", "DEBUG")

    log.info("Creating game window")
    window = GameWindow()
    log.info("Game window created")
    log.info("Starting game window")
    window.start()  # Start the main game loop
    log.info("Game window closed")
