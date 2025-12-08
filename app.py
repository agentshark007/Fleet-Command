from panda2d import PandaWindow, Color, Font, Image, Sound, Key, Anchor, Resizable
import math
from teams import *
from units import *
from utility import distance
from enum import Enum
import random


# Utility classes
class ExtendDirection(Enum):
    LEFT = -1   # Used for horizontal extension
    RIGHT = 1   # Used for horizontal extension
    UP = 1      # Used for vertical extension
    DOWN = -1   # Used for vertical extension


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


    # Utility functions
    def extend(self, pivot, value, direction: ExtendDirection):
        return pivot + (value * direction.value * self.gui_scale)


    def initialize(self):
        self._initialize_settings()
        self._initialize_state_variables()
        self._initialize_game_logic()
        self._initialize_layout()
        self._load_assets()


    def _initialize_settings(self):
        # GUI scale
        self.gui_scale_factor = 20.0
        self.gui_scale_offset = 1.0
        self.gui_scale_min = 0.3
        self.gui_scale_max = 5


    def _initialize_state_variables(self):
        # GUI scale key state tracking
        self.plus_last_frame = False
        self.minus_last_frame = False
        self.gui_scale = 1.0


    def _initialize_game_logic(self):
        self.team_types = [RedFleet(), BlueAlliance(), GreenSquadron(), YellowLegion(), PurpleVanguard(), OrangeCrew(), CyanForce()]
        self.unit_types = [Battleship]
        

        team_count = 5
        team_count = max([len(self.team_types), team_count]) # Ensure ValueError doesn't occor by capping team_count by how many teams there are.

        self.teams = random.sample(self.team_types, team_count)
        self.units = []


    def _initialize_layout(self):
        # GUI shapes
        self.side_panel_color = Color(0, 0, 144, 200)
        self.middle_panel_color = Color(0, 0, 70, 200)
        self.panel_outline_color = Color(0, 0, 100, 50)
        self.title_text_color = Color(100, 100, 20)

        # GUI shapes
        self.panel_outline_thickness = 2
        self.side_panel_roundness = 15


    def _load_assets(self):
        # Fonts
        self.title_font = Font("assets/fonts/BlackOpsOne-Regular.ttf", size=32)
        self.context_font = Font("assets/fonts/WDXLLubrifontSC-Regular.ttf", size=16)
        
        # Images
        self.water_image = Image("assets/images/water.jpg")
        self.water_image_scale = 0.3
        self.selection_arrow_image = Image("assets/images/selection-arrow.png")
        self.target_image = Image("assets/images/target.png")



    def update(self):
        self._update_gui_scale()


    def _update_gui_scale(self):
        growth = self.gui_scale_offset + self.gui_scale_factor * self.deltatime
        command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

        # Get input
        if command_down:
            if self.keydown(Key.EQUALS) and not self.plus_last_frame:
                self.gui_scale *= growth

            elif self.keydown(Key.MINUS) and not self.minus_last_frame:
                self.gui_scale /= growth

        # Clamp gui scale
        self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))

        # Set plus/minus down last frame variables
        self.plus_last_frame = self.keydown(Key.EQUALS)
        self.minus_last_frame = self.keydown(Key.MINUS)



    def draw(self):
        self.clear(Color(0, 0, 0))
        self._draw_ui_panels()


    def _draw_ui_panels(self):
        # Left side panel
        self.fill_rounded_rect(
            self.screen_left,
            self.screen_bottom,
            self.extend(self.screen_left, 150, ExtendDirection.RIGHT),
            self.extend(self.screen_bottom, 100, ExtendDirection.UP),
            color=self.side_panel_color,
            outline_thickness=self.panel_outline_thickness * self.gui_scale,
            outline_color=self.panel_outline_color,
            topleft_roundness=0,
            topright_roundness=self.side_panel_roundness * self.gui_scale,
            bottomleft_roundness=0,
            bottomright_roundness=0
        )
        # Right side panel
        self.fill_rounded_rect(
            self.extend(self.screen_right, 150, ExtendDirection.LEFT),
            self.screen_bottom,
            self.screen_right,
            self.extend(self.screen_bottom, 100, ExtendDirection.UP),
            color=self.side_panel_color,
            outline_thickness=self.panel_outline_thickness * self.gui_scale,
            outline_color=self.panel_outline_color,
            topleft_roundness=self.side_panel_roundness * self.gui_scale,
            topright_roundness=0,
            bottomleft_roundness=0,
            bottomright_roundness=0
        )
        # Bottom command panel
        self.fill_rect(
            self.extend(self.screen_left, 150, ExtendDirection.RIGHT),
            self.screen_bottom,
            self.extend(self.screen_right, 150, ExtendDirection.LEFT),
            self.extend(self.screen_bottom, 80, ExtendDirection.UP),
            color=self.middle_panel_color,
            outline_thickness=self.panel_outline_thickness * self.gui_scale,
            outline_color=self.panel_outline_color
        )
        # Top menu panel
        self.fill_rect(
            self.screen_left,
            self.screen_top,
            self.screen_right,
            self.extend(self.screen_top, 30, ExtendDirection.DOWN),
            color=self.middle_panel_color,
            outline_thickness=self.panel_outline_thickness * self.gui_scale,
            outline_color=self.panel_outline_color
        )
