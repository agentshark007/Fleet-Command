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
    self.mainmenu_button_extend_y = 100  # Pixels from top edge
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
    """Update main menu logic (handle button clicks).
    
    Checks for button clicks and transitions to the appropriate game state.
    """
    # Define all menu buttons: (id, label)
    buttons = [
        ("newgame", "New Game"),
        ("settings", "Settings"),
        ("quit", "Quit")
    ]
    
    # Check each button for clicks
    for i, (button_id, button_label) in enumerate(buttons):
        # Calculate button position
        button_x = self.extend(self.screen_left, self.mainmenu_button_extend_x, ExtendDirection.RIGHT)
        button_y = self.extend(
            self.screen_top,
            self.mainmenu_button_extend_y + i * (self.mainmenu_button_height + self.mainmenu_button_spacing),
            ExtendDirection.DOWN
        )

        # Detect button click and handle per button
        if detect_mainmenu_button(self, button_x, button_y):
            handle_mainmenu_button_action(self, button_id)
            self.mousedownprimary = False  # Prevent multiple triggers on hold


def detect_mainmenu_button(self, x, y):
    """Check if a button was clicked.
    
    Args:
        x: Button left edge position.
        y: Button bottom edge position.
        
    Returns:
        True if the button is under the mouse and the left mouse button is pressed.
    """
    # Calculate button boundaries
    left = x
    bottom = y
    right = self.extend(left, self.mainmenu_button_width, ExtendDirection.RIGHT)
    top = self.extend(bottom, self.mainmenu_button_height, ExtendDirection.UP)

    # Check if mouse is in button area and button is clicked
    if mouse_in_area(self.mousex, self.mousey, left, right, bottom, top) and self.mousedownprimary:
        return True
    return False

def handle_mainmenu_button_action(self, button_id):
    """Execute the action for a clicked button.
    
    Args:
        button_id: The identifier string of the button that was clicked.
    """
    if button_id == "newgame":
        self.game_state = GameState.GAME  # Start new game
    elif button_id == "settings":
        self.game_state = GameState.SETTINGS  # Open settings menu
    elif button_id == "quit":
        quit()  # Exit the application



def draw(self):
    """Render the main menu frame."""
    draw_mainmenu(self)

def draw_mainmenu(self):
    """Render the main menu: background, buttons, and labels."""
    # Dark blue background (fills entire screen)
    self.fill_rect(
        self.screen_left,
        self.screen_bottom,
        self.screen_right,
        self.screen_top,
        color=self.mainmenu_background_color
    )

    # Define all menu buttons: (identifier, label)
    buttons = [
        ("newgame", "New Game"),
        ("settings", "Settings"),
        ("quit", "Quit")
    ]
    
    # Render each button and its label
    for i, (button_id, button_text) in enumerate(buttons):
        # Calculate button position
        button_x = self.extend(self.screen_left, self.mainmenu_button_extend_x, ExtendDirection.RIGHT)
        button_y = self.extend(
            self.screen_top,
            self.mainmenu_button_extend_y + i * (self.mainmenu_button_height + self.mainmenu_button_spacing),
            ExtendDirection.DOWN
        )

        # Draw button rectangle
        draw_mainmenu_button(self, button_x, button_y)

        # Draw button text (centered on button, scaled with GUI scale)
        self.draw_text(
            button_text,
            x=(button_x + (self.mainmenu_button_width / 2)) * self.gui_scale,
            y=(button_y + (self.mainmenu_button_height / 2)) * self.gui_scale,
            font=self.context_font.new_size(int(20 * self.gui_scale)),
            color=Color(255, 255, 255),
            anchor=Anchor.CENTER
        )


def draw_mainmenu_button(self, x, y):
    """Render a single rounded main menu button at `(x, y)`.
    
    Changes color based on hover state.
    
    Args:
        x: Button left edge position.
        y: Button bottom edge position.
    """
    # Calculate button boundaries
    left = x
    bottom = y
    right = self.extend(left, self.mainmenu_button_width, ExtendDirection.RIGHT)
    top = self.extend(bottom, self.mainmenu_button_height, ExtendDirection.UP)

    # Determine button color based on hover state
    if mouse_in_area(self.mousex, self.mousey, left, right, bottom, top):
        button_color = self.mainmenu_button_color_hover  # Bright blue when hovered
    else:
        button_color = self.mainmenu_button_color  # Normal blue when not hovered

    # Draw rounded rectangle button
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
