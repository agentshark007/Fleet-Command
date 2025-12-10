"""Main application entry point for Fleet Command game.

This module contains the GameWindow class which serves as the main game window
and orchestrates the game loop, state management, and rendering across different
game states (main menu, new game, gameplay, paused, settings).
"""

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


class GameWindow(PandaWindow):
    """Main game window that manages the game loop and state transitions.
    
    This class inherits from PandaWindow and orchestrates all game systems including
    initialization, update logic, and rendering for different game states.
    """
    def __init__(self):
        """Initialize the game window with default dimensions and settings."""
        super().__init__(
            width=800,
            height=600,
            title="Fleet Command",
            resizable=Resizable.BOTH,
            anchor=Anchor.CENTER
        )

    def extend(self, pivot, value, direction: ExtendDirection):
        """Extend a position in a given direction by a scaled amount.
        
        Args:
            pivot: Starting position (x or y coordinate).
            value: Distance to extend from pivot.
            direction: ExtendDirection enum specifying the direction (LEFT, RIGHT, UP, DOWN).
            
        Returns:
            The new position after extending and applying GUI scale.
        """
        return pivot + (value * direction.value * self.gui_scale)


    def initialize(self):
        """Initialize all game subsystems and UI modules.
        
        Called once at startup to set up core systems, game logic, and all game states.
        """
        self.menu_state = GameState.MAINMENU # Current game state tracking

        core.initialize(self)  # Initialize core systems (assets, GUI scale)
        game.initialize(self)  # Initialize gameplay systems
        mainmenu.initialize(self)  # Initialize main menu UI
        newgame.initialize(self)  # Initialize new game screen
        paused.initialize(self)  # Initialize pause menu
        settings.initialize(self)  # Initialize settings menu


    def update(self):
        """Update game logic based on the current game state.
        
        This is called once per frame and routes update calls to the appropriate
        game state handler based on the current menu_state.
        """
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
        """Render the current game state to the screen.
        
        This is called once per frame after update() and routes drawing calls
        to the appropriate state renderer.
        """
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



def main():
    """Entry point for the application.
    
    Creates the main game window and starts the game loop.
    """
    window = GameWindow()
    window.start()  # Start the main game loop
