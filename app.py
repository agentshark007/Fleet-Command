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


class Camera():
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.velocity_x = 0
        self.velocity_y = 0

    def project(self, x, y):
        """
        Converts x/y worldspace position into screenspace position.
        
        :param self: Class self
        :param x: Worldspace X position
        :param y: Worldspace Y position
        """
        x = (x - self.x) * self.scale
        y = (y - self.y) * self.scale

        return x, y
    
    def deduce(self, x, y):
        """
        Converts x/y screenspace position into worldspace position.
        
        :param self: Class self
        :param x: Screenspace X position
        :param y: Screenspace Y position
        """
        x = x / self.scale + self.x
        y = y / self.scale + self.y

        return x, y


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
        self.gui_scale_max = 5.0

        # Water
        self.water_state_speed = 10

        # Camera control
        self.camera_zoom_speed = 0.1
        self.min_camera_scale = 0.3
        self.max_camera_scale = 3.0
        self.camera_move_speed = 100.0
        self.camera_move_friction = 0.9


    def _initialize_state_variables(self):
        # GUI scale key state tracking
        self.plus_last_frame = False
        self.minus_last_frame = False
        self.gui_scale = 1.0

        # Water
        self.water_state = 0

        # Camera
        self.camera = Camera(0.0, 0.0, 1.0)


    def _initialize_game_logic(self):
        self.team_types = [RedFleet(), BlueAlliance(), GreenSquadron(), YellowLegion(), PurpleVanguard(), OrangeCrew(), CyanForce()]
        self.unit_types = [Battleship]
        

        team_count = 5
        team_count = min([len(self.team_types), team_count]) # Ensure ValueError doesn't occor by capping team_count by how many teams there are.

        self.teams = random.sample(self.team_types, team_count)
        self.units = []
        print(self.teams)


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
        self.autonomous_target_image = Image("assets/images/target.png")



    def update(self):
        self._handle_plus_minus_input()
        self._handle_camera_movement()
        self._update_water()
        print(self.camera.scale)


    def _handle_plus_minus_input(self):
        # Calculate gui scale growth
        growth = self.gui_scale_offset + self.gui_scale_factor * self.deltatime

        # Detect if either command key held down
        command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

        # Get -/+ input
        if command_down:
            if self.keydown(Key.EQUALS) and not self.plus_last_frame:
                self.gui_scale *= growth

            elif self.keydown(Key.MINUS) and not self.minus_last_frame:
                self.gui_scale /= growth
        else:
            if self.keydown(Key.EQUALS) and not self.plus_last_frame:
                self.camera.scale = min([self.max_camera_scale, self.camera.scale + self.camera_zoom_speed])

            elif self.keydown(Key.MINUS) and not self.minus_last_frame:
                self.camera.scale = max([self.min_camera_scale, self.camera.scale - self.camera_zoom_speed])

        # Clamp gui scale
        self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))

        # Set plus/minus down last frame variables
        self.plus_last_frame = self.keydown(Key.EQUALS)
        self.minus_last_frame = self.keydown(Key.MINUS)


    def _handle_camera_movement(self):
        # Accelerate
        if self.keydown(Key.LEFT):
            self.camera.velocity_x -= self.camera_move_speed * self.deltatime
        if self.keydown(Key.RIGHT):
            self.camera.velocity_x += self.camera_move_speed * self.deltatime
        if self.keydown(Key.UP):
            self.camera.velocity_y += self.camera_move_speed * self.deltatime
        if self.keydown(Key.DOWN):
            self.camera.velocity_y -= self.camera_move_speed * self.deltatime

        # Friction
        self.camera.velocity_x *= self.camera_move_friction
        self.camera.velocity_y *= self.camera_move_friction

        # Update position
        self.camera.x += self.camera.velocity_x
        self.camera.y += self.camera.velocity_y


    def _update_water(self):
        self.water_state += self.water_state_speed * self.deltatime



    def draw(self):
        self.clear(Color(0, 0, 0))
        self._draw_water()
        self._draw_ui_panels()


    def _draw_water(self):
        def draw_water(filter: Color = Color(255, 255, 255, 255)):
            camera_zoom = self.camera.scale
            scale = self.water_image_scale * self.gui_scale * camera_zoom
            width = self.water_image.get_width()
            height = self.water_image.get_height()
            tile_w = width * scale - 1  # Subtract 1 to prevent gaps
            tile_h = height * scale - 1

            # Calculate offset for seamless tiling
            offset_x = (self.camera.x * scale) % tile_w
            offset_y = (self.camera.y * scale) % tile_h

            # Calculate tiling bounds to always cover screen
            x_start = self.screen_left - offset_x - tile_w
            y_start = self.screen_bottom - offset_y - tile_h
            x_end = self.screen_right
            y_end = self.screen_top
            cols = int(math.ceil((x_end - x_start) / tile_w)) + 1
            rows = int(math.ceil((y_end - y_start) / tile_h)) + 1

            for col in range(cols):
                for row in range(rows):
                    x = x_start + col * tile_w
                    y = y_start + row * tile_h
                    self.draw_image(
                        self.water_image,
                        x,
                        y,
                        anchor=Anchor.BOTTOMLEFT,
                        xscale=scale,
                        yscale=scale,
                        filter=filter,
                        rotation=0
                    )

        draw_water()



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
