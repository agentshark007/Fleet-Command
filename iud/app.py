from core.enums import ExtendDirection, GameState
from iud import core, game, mainmenu, newgame, paused, settings
from libraries import log
from libraries.pgiud import *


class GameWindow(Window):
    gui_scale: float = 1.0

    def __init__(self) -> None:
        super().__init__(width=800, height=600, title='Fleet Command',
                         resizable=Resizable.BOTH, origin=Origin.CENTER)
        self.gui_scale = 1.0

    def extend(self, pivot, value, direction: ExtendDirection):
        return pivot + value * direction.value * self.gui_scale

    def initialize(self):
        log.info('Global initialization started')
        self.menu_state = GameState.MAINMENU
        core.initialize(self)
        game.initialize(self)
        mainmenu.initialize(self)
        newgame.initialize(self)
        paused.initialize(self)
        settings.initialize(self)
        core.late_initialize(self)
        log.info('Global initialization complete')

    def update(self):
        core.update(self)
        match self.menu_state:
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
        core.draw(self)
        match self.menu_state:
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
        core.late_draw(self)


def main():
    log.reset('fleet-command.log', 'WARN')
    log.info('Creating game window')
    window = GameWindow()
    log.info('Game window created')
    log.info('Starting game window')
    window.start()
    log.info('Game window closed')
