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
        self.water_state_speed = 5

        # Camera control
        self.camera_zoom_speed = 0.1
        self.min_camera_scale = 0.3
        self.max_camera_scale = 3.0
        self.camera_move_speed = 30.0
        self.camera_move_friction = 0.9

        # Image scales
        self.selection_arrow_scale = 0.05
        self.selection_distance = 100
        self.autonomous_target_image_scale = 0.05


    def _initialize_state_variables(self):
        # GUI scale key state tracking
        self.plus_last_frame = False
        self.minus_last_frame = False
        self.gui_scale = 1.0

        # Water
        self.water_state = 0

        # Camera
        self.camera = Camera(0.0, 0.0, 1.0)

        # Selection
        self.selected_unit_index = -1 # -1 means none selected


    def _initialize_game_logic(self):
        self.unit_types = [Battleship]

        team_count = 4
        self.teams = random_teams(team_count)
        self.units = [Battleship(team_index=random.randint(0, len(self.teams) - 1), position_x=random.uniform(-1000, 1000), position_y=random.uniform(-1000, 1000), direction=random.uniform(0, 360)) for _ in range(20)]


    def _initialize_layout(self):
        # GUI colors
        self.side_panel_color = Color(0, 0, 144, 150)
        self.middle_panel_color = Color(0, 0, 70, 150)
        self.panel_outline_color = Color(0, 0, 100, 50)
        self.title_text_color = Color(100, 100, 20)

        # GUI shapes
        self.panel_outline_thickness = 2
        self.side_panel_roundness = 15

        # Game filters
        self.other_unit_filter = Color(150, 150, 150, 255)
        self.hover_unit_filter = Color(200, 200, 200, 255)
        self.selected_unit_filter = Color(255, 255, 255, 255)


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
        self._handle_selection_input()
        self._handle_camera_movement()
        self._update_water()


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


    def _handle_selection_input(self):
        pass


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
        self._draw_units()
        self._draw_ui_panels()


    def _draw_tiled_water(self, filter_color: Color, offset_x: float = 0.0, offset_y: float = 0.0):
        offset = 5 # Pixels to overlap tiles by to avoid gaps

        # World-space tiling; no gaps; zoom centered
        world_tile_w = (self.water_image.get_width() - offset) * self.water_image_scale * self.gui_scale
        world_tile_h = (self.water_image.get_height() - offset) * self.water_image_scale * self.gui_scale

        screen_w = self.screen_right - self.screen_left
        screen_h = self.screen_top - self.screen_bottom

        # Effective camera position with offsets (simulate camera movement)
        eff_cam_x = self.camera.x + offset_x
        eff_cam_y = self.camera.y + offset_y

        # Convert screen edges to world coordinates using effective camera
        world_left = self.screen_left / self.camera.scale + eff_cam_x
        world_bottom = self.screen_bottom / self.camera.scale + eff_cam_y
        world_right = self.screen_right / self.camera.scale + eff_cam_x
        world_top = self.screen_top / self.camera.scale + eff_cam_y

        start_world_x = world_left - (world_left % world_tile_w) - world_tile_w
        start_world_y = world_bottom - (world_bottom % world_tile_h) - world_tile_h

        tile_w_screen = world_tile_w * self.camera.scale
        tile_h_screen = world_tile_h * self.camera.scale
        cols = int(math.ceil(screen_w / tile_w_screen)) + 3
        rows = int(math.ceil(screen_h / tile_h_screen)) + 3

        xscale = self.water_image_scale * self.gui_scale * self.camera.scale
        yscale = xscale

        for col in range(cols):
            for row in range(rows):
                wx = start_world_x + col * world_tile_w
                wy = start_world_y + row * world_tile_h
                # Project with effective camera by subtracting offsets
                sx, sy = self.camera.project(wx - offset_x, wy - offset_y)
                self.draw_image(
                    self.water_image,
                    sx,
                    sy,
                    anchor=Anchor.BOTTOMLEFT,
                    xscale=xscale,
                    yscale=yscale,
                    filter=filter_color,
                    rotation=0
                )

    def _draw_units(self):
        # Calculate mouse world position
        mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)

        # Get closest unit to mouse
        closest_unit_index = -1
        closest_unit_index_selectable = -1
        closest_distance = float('inf')
        closest_distance_selectable = float('inf')
        for index, unit in enumerate(self.units):
            dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
            if dist < closest_distance:
                closest_distance = dist
                closest_unit_index = index
            if dist < closest_distance_selectable and dist < self.selection_distance:
                closest_distance_selectable = dist
                closest_unit_index_selectable = index

        # Draw units
        for index, unit in enumerate(self.units):
            # Calculate the screen position of the unit
            screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
            
            # Draw the unit
            if index == self.selected_unit_index:
                # Selected unit
                self.draw_image(
                    unit.image,
                    screen_x,
                    screen_y,
                    anchor=Anchor.CENTER,
                    xscale=0.5 * self.gui_scale * self.camera.scale,
                    yscale=0.5 * self.gui_scale * self.camera.scale,
                    filter=self.selected_unit_filter,
                    rotation=unit.direction
                )

                if unit.autonomous:
                    # Draw autonomous target
                    target_screen_x, target_screen_y = self.camera.project(unit.autonomous_target_x, unit.autonomous_target_y)
                    self.draw_image(
                        self.autonomous_target_image,
                        target_screen_x,
                        target_screen_y,
                        anchor=Anchor.CENTER,
                        xscale=self.autonomous_target_image_scale * self.gui_scale * self.camera.scale,
                        yscale=self.autonomous_target_image_scale * self.gui_scale * self.camera.scale,
                        rotation=0
                    )
            elif index == closest_unit_index_selectable:
                # Hovered unit
                self.draw_image(
                    unit.image,
                    screen_x,
                    screen_y,
                    anchor=Anchor.CENTER,
                    xscale=0.5 * self.gui_scale * self.camera.scale,
                    yscale=0.5 * self.gui_scale * self.camera.scale,
                    filter=self.hover_unit_filter,
                    rotation=unit.direction
                )
            else:
                # Other units
                self.draw_image(
                    unit.image,
                    screen_x,
                    screen_y,
                    anchor=Anchor.CENTER,
                    xscale=0.5 * self.gui_scale * self.camera.scale,
                    yscale=0.5 * self.gui_scale * self.camera.scale,
                    filter=self.other_unit_filter,
                    rotation=unit.direction
                )

        # Draw unit team arrows
        for index, unit in enumerate(self.units):
            # Calculate the screen position of the arrow
            screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
            
            # Draw the arrow
            self.draw_image(
                self.selection_arrow_image,
                screen_x,
                screen_y + 100 * self.gui_scale * self.camera.scale,
                anchor=Anchor.BOTTOM,
                xscale=self.selection_arrow_scale * self.gui_scale * self.camera.scale,
                yscale=self.selection_arrow_scale  * self.gui_scale * self.camera.scale,
                filter=self.teams[unit.team_index].color.color,
                rotation=0
            )


    def _draw_water(self):
        # Simulate water movement by offsetting the tiling based on water state and also moving other layers in different ways
        
        # Base layer, not moving
        self._draw_tiled_water(
            Color(170, 150, 150, 255),
            0.0,
            0.0
        )

        # Second layer, moving in one direction
        self._draw_tiled_water(
            Color(150, 170, 150, 200),
            self.water_state * -2,
            self.water_state * -2
        )

        # Third layer, moving in a circle
        self._draw_tiled_water(
            Color(150, 150, 170, 120),
            math.cos(self.water_state * 0.1) * 20.0,
            math.sin(self.water_state * 0.1) * 20.0
        )




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
