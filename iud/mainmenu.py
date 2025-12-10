from panda2d import *
from core.enums import ExtendDirection
from core.utility import mouse_in_area
from core.enums import GameState

def initialize(self):
    self.mainmenu_button_extend_x = 50
    self.mainmenu_button_extend_y = 100
    self.mainmenu_button_spacing = 20
    self.mainmenu_button_width = 150
    self.mainmenu_button_height = 60
    self.mainmenu_button_roundness = 15

    self.mainmenu_background_color = Color(0, 0, 50)
    self.mainmenu_button_color = Color(0, 0, 100)
    self.mainmenu_button_color_hover = Color(30, 30, 130)
    self.mainmenu_button_outline_thickness = 2
    self.mainmenu_button_outline_color = Color(0, 0, 0)



def update(self):
    # Centralized menu: (identifier, label)
    buttons = [
        ("newgame", "New Game"),
        ("settings", "Settings"),
        ("quit", "Quit")
    ]
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
    left = x
    bottom = y
    right = self.extend(left, self.mainmenu_button_width, ExtendDirection.RIGHT)
    top = self.extend(bottom, self.mainmenu_button_height, ExtendDirection.UP)

    if mouse_in_area(self.mousex, self.mousey, left, right, bottom, top) and self.mousedownprimary:
        return True
    return False

def handle_mainmenu_button_action(self, button_id):
    if button_id == "newgame":
        self.game_state = GameState.GAME  # Or GameState.NEWGAME if you have a new game state
    elif button_id == "settings":
        self.game_state = GameState.SETTINGS
    elif button_id == "quit":
        quit()



def draw(self):
    draw_mainmenu(self)

def draw_mainmenu(self):
    """Render the main menu: background, buttons, and labels."""
    # Dark blue background
    self.fill_rect(
        self.screen_left,
        self.screen_bottom,
        self.screen_right,
        self.screen_top,
        color=self.mainmenu_background_color
    )

    # Centralized menu: (identifier, label)
    buttons = [
        ("newgame", "New Game"),
        ("settings", "Settings"),
        ("quit", "Quit")
    ]
    for i, (button_id, button_text) in enumerate(buttons):
        # Calculate button position
        button_x = self.extend(self.screen_left, self.mainmenu_button_extend_x, ExtendDirection.RIGHT)
        button_y = self.extend(
            self.screen_top,
            self.mainmenu_button_extend_y + i * (self.mainmenu_button_height + self.mainmenu_button_spacing),
            ExtendDirection.DOWN
        )

        # Draw button
        draw_mainmenu_button(self, button_x, button_y)

        # Draw button text (centered, scaling applied to position and font)
        self.draw_text(
            button_text,
            x=(button_x + (self.mainmenu_button_width / 2)) * self.gui_scale,
            y=(button_y + (self.mainmenu_button_height / 2)) * self.gui_scale,
            font=self.context_font.new_size(int(20 * self.gui_scale)),
            color=Color(255, 255, 255),
            anchor=Anchor.CENTER
        )


def draw_mainmenu_button(self, x, y):
    """Render a single rounded main menu button at `(x, y)`."""
    left = x
    bottom = y
    right = self.extend(left, self.mainmenu_button_width, ExtendDirection.RIGHT)
    top = self.extend(bottom, self.mainmenu_button_height, ExtendDirection.UP)

    if mouse_in_area(self.mousex, self.mousey, left, right, bottom, top):
        # Hovered button color
        button_color = self.mainmenu_button_color_hover
    else:
        # Normal button color
        button_color = self.mainmenu_button_color

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
