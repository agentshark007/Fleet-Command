"""Main menu UI module for Fleet Command.

This module handles the main menu state including initialization,
button detection, button actions, and rendering of the menu.
"""

from panda2d import *
from core.enums import ExtendDirection
from core.utility import mouse_in_area
from core.enums import GameState

def initialize(self):
    """Initialize main menu configuration and button layout settings."""
    # Button positioning
    self.mainmenu_button_extend_x = 50  # Pixels from left edge
    self.mainmenu_button_extend_y = 50  # Pixels from bottom edge
    self.mainmenu_button_spacing = 20  # Pixels between buttons
    self.mainmenu_button_width = 150  # Button width in pixels
    self.mainmenu_button_height = 60  # Button height in pixels
    self.mainmenu_button_roundness = 15  # Corner radius in pixels

    # Color scheme
    self.mainmenu_background_color = Color(0, 0, 50)  # Dark blue background
    self.mainmenu_button_color = Color(0, 0, 100)  # Normal button color
    self.mainmenu_button_color_hover = Color(30, 30, 130)  # Hovered button color
    self.mainmenu_button_outline_thickness = 2  # Button border width
    self.mainmenu_button_outline_color = Color(0, 0, 0)  # Black border



def update(self):
    """Handle main menu button interactions."""
    # Define button actions
    buttons = [
        ("newgame", newgame),
        ("settings", settings),
        ("quit", quit)
    ]
    
    for index, (button_id, action) in enumerate(reversed(buttons)):
        left, bottom, right, top = get_button_bounds(self, index)
        
        if mouse_in_area(self.mousex, self.mousey, left, right, bottom, top):
            if self.mousedownprimary:
                action(self)
                break

def newgame(self):
    """Transition to the new game setup state."""
    self.menu_state = GameState.GAME

def settings(self):
    """Transition to the settings menu state."""
    self.menu_state = GameState.SETTINGS



def draw(self):
    """Render the main menu frame."""
    # Draw background
    self.fill_rect(
        self.screen_left,
        self.screen_bottom,
        self.screen_right,
        self.screen_top,
        color=self.mainmenu_background_color
    )

    # Define menu buttons
    buttons = [
        ("newgame", "New Game"),
        ("settings", "Settings"),
        ("quit", "Quit")
    ]
    
    for index, (button_id, button_text) in enumerate(buttons):
        # Draw button and text
        draw_button(self, button_text, index, len(buttons))


def get_button_bounds(self, index):
    button_left = self.extend(
        self.screen_left,
        self.mainmenu_button_extend_x,
        ExtendDirection.RIGHT
    )
    button_bottom = self.extend(
        self.screen_bottom,
        self.mainmenu_button_extend_y,
        ExtendDirection.UP
    )
    button_right = self.extend(
        button_left,
        self.mainmenu_button_width,
        ExtendDirection.RIGHT
    )
    button_top = self.extend(
        button_bottom,
        self.mainmenu_button_height,
        ExtendDirection.UP
    )

    spacing = (self.mainmenu_button_spacing + self.mainmenu_button_height) * self.gui_scale
    vertical_offset = spacing * index

    left = button_left
    bottom = button_bottom + vertical_offset  # Add offset, don't multiply
    right = button_right
    top = button_top + vertical_offset

    return left, bottom, right, top


def draw_button(self, text, index, max_index):
    """Draw a button with text.
    
    Args:
        x: Button left edge position.
        y: Button bottom edge position.
        text: Button label text.
    """
    # Get button bounds
    left, bottom, right, top = get_button_bounds(self, max_index - index - 1)
    
    # Determine button color based on hover state
    button_color = (
        self.mainmenu_button_color_hover
        if mouse_in_area(self.mousex, self.mousey, left, right, bottom, top)
        else self.mainmenu_button_color
    )

    # Draw button background
    self.fill_rounded_rect(
        left,
        bottom,
        right,
        top,
        color=button_color,
        outline_thickness=self.mainmenu_button_outline_thickness * self.gui_scale,
        outline_color=self.mainmenu_button_outline_color,
        topleft_roundness=self.mainmenu_button_roundness * self.gui_scale,
        topright_roundness=self.mainmenu_button_roundness * self.gui_scale,
        bottomleft_roundness=self.mainmenu_button_roundness * self.gui_scale,
        bottomright_roundness=self.mainmenu_button_roundness * self.gui_scale
    )

    # Draw button text
    self.draw_text(
        text,
        x=(left + right) / 2,
        y=(bottom + top) / 2,
        font=self.context_font.new_size(int(20 * self.gui_scale)),
        color=Color(255, 255, 255),
        anchor=Anchor.CENTER
    )
