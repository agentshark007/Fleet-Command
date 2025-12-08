from panda2d import PandaWindow, Color, Font, Image, Sound, Key, Anchor, Resizable
import math
from extention import Extension, ExtendMethod
from teams import RedFleet, BlueAlliance, GreenSquadron
from units import Battleship
from utility import distance


class GameWindow(PandaWindow):
    """Main window for Fleet Command game."""

    def __init__(self):
        super().__init__(
            width=800,
            height=600,
            title="Fleet Command",
            resizable=Resizable.BOTH,
            anchor=Anchor.CENTER
        )


    def initialize(self):
        """Initialize game resources and UI settings."""
        self._init_resources()

    def _init_resources(self):
        # Extension logic
        self.extension = Extension()
        self.extension.scale = 1.0

        # Camera zoom
        self.camera_zoom = 1.0

        # Extension scaling factors
        self.extension_change_factor = 20.0
        self.extension_change_offset = 1.0

        # Track key state for scaling
        self.plus_last_frame = False
        self.minus_last_frame = False

        # Fonts & Images
        self.title_font = Font("assets/fonts/BlackOpsOne-Regular.ttf", size=32)
        self.context_font = Font("assets/fonts/WDXLLubrifontSC-Regular.ttf", size=16)
        self.water_image = Image("assets/images/water.jpg")
        self.water_image_scale = 0.3
        self.selection_arrow_image = Image("assets/images/selection-arrow.png")
        self.target_image = Image("assets/images/target.png")

        # UI Colors & Panel Settings
        self.side_panel_color = Color(0, 0, 144, 200)
        self.middle_panel_color = Color(0, 0, 70, 200)
        self.panel_outline_color = Color(0, 0, 100, 50)
        self.panel_outline_thickness = 2
        self.side_panel_roundness = 15
        self.title_text_color = Color(100, 100, 20)
        self.title_text_shadow_color = Color(0, 20, 0, 130)
        self.title_text_shadow_offset = 1

        # Screen position tracking
        self.camera_position_x = 0
        self.camera_position_y = 0
        self.camera_move_speed = 200

        # Water layer position
        self.water_layer_position = 100
        self.water_layer_position_speed = 10

        # Teams
        self.teams = [RedFleet(), BlueAlliance(), GreenSquadron()]

        # Units
        self.units = [Battleship(self.teams[0], 100, 100, 267), Battleship(self.teams[1], -100, 200, 20), Battleship(self.teams[2], 50, -150, -50)]

        # Selection
        self.selected_unit_index = -1
        self.selected_unit_target_position = (0, 0)
        self.unit_select_distance = 100  # Distance threshold for selecting a unit



    def update(self):
        """Update game state and handle input."""
        self._handle_input()
        self._update_water_layer()
        self._update_unit_selection()
        self._update_unit_input()
        self._update_unit_movement()

    def _handle_input(self):
        growth = self.extension_change_offset + self.extension_change_factor * self.deltatime
        zoom_speed = 0.1
        command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)
        if command_down:
            if self.keydown(Key.EQUALS) and not self.plus_last_frame:
                self.extension.scale *= growth
                self.plus_last_frame = True
            elif self.keydown(Key.MINUS) and not self.minus_last_frame:
                self.extension.scale /= growth
                self.minus_last_frame = True
        else:
            if self.keydown(Key.EQUALS) and not self.plus_last_frame:
                self.camera_zoom += zoom_speed
                self.plus_last_frame = True
            elif self.keydown(Key.MINUS) and not self.minus_last_frame:
                self.camera_zoom = max(0.1, self.camera_zoom - zoom_speed)
                self.minus_last_frame = True
        if not self.keydown(Key.EQUALS):
            self.plus_last_frame = False
        if not self.keydown(Key.MINUS):
            self.minus_last_frame = False
        if self.keydown(Key.LEFT):
            self.camera_position_x += self.camera_move_speed * self.deltatime
        if self.keydown(Key.RIGHT):
            self.camera_position_x -= self.camera_move_speed * self.deltatime
        if self.keydown(Key.UP):
            self.camera_position_y -= self.camera_move_speed * self.deltatime
        if self.keydown(Key.DOWN):
            self.camera_position_y += self.camera_move_speed * self.deltatime

    def _update_water_layer(self):
        self.water_layer_position += self.water_layer_position_speed * self.deltatime
        if self.water_layer_position > 200:
            self.water_layer_position = 0

    def _update_unit_selection(self):
        closest_unit_index = -1
        closest_distance = float('inf')
        # Transform mouse position to world coordinates considering scale and zoom
        mouse_world_x = (self.mousex - self.screen_center_x) / (self.extension.scale * self.camera_zoom) - self.camera_position_x
        mouse_world_y = (self.mousey - self.screen_center_y) / (self.extension.scale * self.camera_zoom) - self.camera_position_y
        for index, unit in enumerate(self.units):
            dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
            if dist < closest_distance:
                closest_distance = dist
                closest_unit_index = index
        if self.mousedownprimary:
            if closest_distance < self.unit_select_distance:
                self.selected_unit_index = closest_unit_index
            else:
                self.selected_unit_index = -1

    def _update_unit_input(self):
        def manual_override():
            return any([
                self.keydown(Key.W),
                self.keydown(Key.S),
                self.keydown(Key.A),
                self.keydown(Key.D)
            ])
        
        def detect_autonomous_activation(unit):
            if self.mousedownsecondary:
                mouse_world_x = (self.mousex - self.screen_center_x) / (self.extension.scale * self.camera_zoom) - self.camera_position_x
                mouse_world_y = (self.mousey - self.screen_center_y) / (self.extension.scale * self.camera_zoom) - self.camera_position_y
                unit.autonomous_target_x = mouse_world_x
                unit.autonomous_target_y = mouse_world_y
                unit.autonomous = True

        def detect_autonomous_deactivation(unit, is_selected):
            if is_selected and manual_override():
                unit.autonomous = False

        def autonomous_input(unit): # Return where autonomous thinks the unit should go
            # Improved autonomous behavior: smooth turning and speed control
            target_x, target_y = unit.autonomous_target_x, unit.autonomous_target_y
            dx = target_x - unit.position_x
            dy = target_y - unit.position_y
            distance_to_target = math.hypot(dx, dy)
            if distance_to_target < 10:
                # Stop if close to target
                return 0, 0
            angle_to_target = math.degrees(math.atan2(dx, dy))
            angle_diff = (angle_to_target - unit.direction + 360) % 360
            if angle_diff > 180:
                angle_diff -= 360
            # Smooth turning: scale rotation by angle difference
            max_turn = unit.rotation_speed
            direction = max(-max_turn, min(max_turn, angle_diff))
            # Slow down when not facing target
            if abs(angle_diff) < 10:
                acceleration = unit.speed
            else:
                acceleration = unit.speed * max(0.2, 1 - abs(angle_diff) / 180)
            return acceleration, direction

        def manual_input(unit): # Return where manual input thinks the unit should go
            acceleration = 0
            direction = 0
            if self.keydown(Key.W):
                acceleration += unit.speed
            if self.keydown(Key.S):
                acceleration -= unit.speed
            if self.keydown(Key.A) and acceleration != 0:
                direction -= unit.rotation_speed
            if self.keydown(Key.D) and acceleration != 0:
                direction += unit.rotation_speed
            return acceleration, direction

        for index, unit in enumerate(self.units):
            # acceleration, direction = 0, 0
            # if unit.autonomous:
            #     acceleration, direction = autonomous_input(unit)

            # if index == self.selected_unit_index:
            #     if not unit.autonomous:
            #         acceleration, direction = manual_input(unit)

            acceleration, direction = 0, 0

            # If selected, check for autonomous activation/deactivation and prioritize manual input
            if index == self.selected_unit_index:
                detect_autonomous_activation(unit)
                detect_autonomous_deactivation(unit, True)
                if not unit.autonomous:
                    acceleration, direction = manual_input(unit)
            # If autonomous is active and not manually controlled, use autonomous input
            if unit.autonomous:
                # Only use autonomous if not selected or selected but not manually controlling
                if index != self.selected_unit_index or (index == self.selected_unit_index and acceleration == 0 and direction == 0):
                    acceleration, direction = autonomous_input(unit)


            # Update unit's velocity and position based on input, whether or not selected or not selected
            unit.velocity_rotation += direction * self.deltatime
            unit.velocity_x += math.sin(math.radians(unit.direction)) * acceleration * self.deltatime
            unit.velocity_y += math.cos(math.radians(unit.direction)) * acceleration * self.deltatime

    def _update_unit_movement(self):
        for index, unit in enumerate(self.units):
            # Apply friction
            unit.velocity_x *= unit.friction
            unit.velocity_y *= unit.friction
            unit.velocity_rotation *= unit.rotation_friction
            
            # Update position and direction
            unit.direction += unit.velocity_rotation * self.deltatime
            unit.position_x += unit.velocity_x * self.deltatime
            unit.position_y += unit.velocity_y * self.deltatime


    def draw(self):
        """Draw all game elements and UI panels."""
        self.clear(Color(0, 0, 0))  # Clear screen each frame
        self._draw_water_background()
        self._draw_units()
        self._draw_ui_panels()
        self._draw_text()
        self._draw_team_info()

    def _draw_water_background(self):
        camera_zoom = self.camera_zoom
        scale = self.water_image_scale * self.extension.scale * camera_zoom
        width = self.water_image.get_width()
        height = self.water_image.get_height()
        tile_w = width * scale - 1 # Subtract 1 to prevent gaps
        tile_h = height * scale - 1

        # Use configurable variables
        filter = Color(200, 200, 200, 255)
        offset_x = self.camera_position_x * self.extension.scale * camera_zoom
        offset_y = self.camera_position_y * self.extension.scale * camera_zoom

        # Offset shrinks as you zoom out
        offset_x = offset_x * camera_zoom * self.extension.scale
        offset_y = offset_y * camera_zoom * self.extension.scale

        # Modulo offset to ensure seamless tiling
        offset_x = offset_x % tile_w
        offset_y = offset_y % tile_h

        # Calculate tiling bounds to always cover screen
        x_start = offset_x - tile_w + self.screen_left
        y_start = offset_y - tile_h + self.screen_bottom
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


        camera_zoom = self.camera_zoom
        scale = self.water_image_scale * self.extension.scale * camera_zoom
        width = self.water_image.get_width()
        height = self.water_image.get_height()
        tile_w = width * scale - 1 # Subtract 1 to prevent gaps
        tile_h = height * scale - 1

        # Use configurable variables
        filter = Color(150, 150, 150, 120)
        offset_x = self.camera_position_x * self.extension.scale * camera_zoom
        offset_y = self.camera_position_y * self.extension.scale * camera_zoom

        # Offset shrinks as you zoom out
        offset_x = offset_x * camera_zoom * self.extension.scale
        offset_y = offset_y * camera_zoom * self.extension.scale

        # Modulo offset to ensure seamless tiling
        offset_x = offset_x % tile_w
        offset_y = offset_y % tile_h

        # Calculate tiling bounds to always cover screen
        x_start = offset_x - tile_w + self.screen_left
        y_start = offset_y - tile_h + self.screen_bottom
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
                    


    def _draw_units(self):
        # Calculate mouse position in world coordinates
        mouse_world_x = (self.mousex - self.screen_center_x) / (self.extension.scale * self.camera_zoom) - self.camera_position_x
        mouse_world_y = (self.mousey - self.screen_center_y) / (self.extension.scale * self.camera_zoom) - self.camera_position_y
        closest_unit_index = -1
        closest_distance = float('inf')
        for index, unit in enumerate(self.units):
            dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
            if dist < closest_distance:
                closest_distance = dist
                closest_unit_index = index
        unit_index = -1
        for unit in self.units:
            unit_index += 1
            screen_x = self.screen_center_x + (unit.position_x + self.camera_position_x) * self.extension.scale * self.camera_zoom
            screen_y = self.screen_center_y + (unit.position_y + self.camera_position_y) * self.extension.scale * self.camera_zoom
            if unit_index == self.selected_unit_index:
                self.draw_image(
                    unit.image,
                    screen_x,
                    screen_y,
                    anchor=Anchor.CENTER,
                    xscale=self.extension.scale * self.camera_zoom,
                    yscale=self.extension.scale * self.camera_zoom,
                    filter=Color(255, 255, 255, 255),
                    rotation=unit.direction
                )

                if unit.autonomous:
                    self.draw_image(
                        self.target_image,
                        self.screen_center_x + (unit.autonomous_target_x + self.camera_position_x) * self.extension.scale * self.camera_zoom,
                        self.screen_center_y + (unit.autonomous_target_y + self.camera_position_y) * self.extension.scale * self.camera_zoom,
                        anchor=Anchor.CENTER,
                        xscale=0.05 * self.extension.scale * self.camera_zoom,
                        yscale=0.05 * self.extension.scale * self.camera_zoom,
                        rotation=0
                    )
            elif unit_index == closest_unit_index and closest_distance < self.unit_select_distance:
                self.draw_image(
                    unit.image,
                    screen_x,
                    screen_y,
                    anchor=Anchor.CENTER,
                    xscale=self.extension.scale * self.camera_zoom,
                    yscale=self.extension.scale * self.camera_zoom,
                    filter=Color(200, 200, 200, 255),
                    rotation=unit.direction
                )
            else:
                self.draw_image(
                    unit.image,
                    screen_x,
                    screen_y,
                    anchor=Anchor.CENTER,
                    xscale=self.extension.scale * self.camera_zoom,
                    yscale=self.extension.scale * self.camera_zoom,
                    filter=Color(150, 150, 150, 255),
                    rotation=unit.direction
                )
            self.draw_image(
                self.selection_arrow_image,
                screen_x,
                screen_y + 150 * self.extension.scale * self.camera_zoom,
                anchor=Anchor.CENTER,
                xscale=self.extension.scale * self.camera_zoom * 0.05,
                yscale=self.extension.scale * self.camera_zoom * 0.05,
                filter=unit.team.color,
                rotation=0
            )

    def _draw_ui_panels(self):
        # Left side panel
        self.fill_rounded_rect(
            self.screen_left,
            self.screen_bottom,
            self.extension.extend(self.screen_left, 150, ExtendMethod.RIGHT),
            self.extension.extend(self.screen_bottom, 100, ExtendMethod.UP),
            color=self.side_panel_color,
            outline_thickness=self.panel_outline_thickness * self.extension.scale,
            outline_color=self.panel_outline_color,
            topleft_roundness=0,
            topright_roundness=self.side_panel_roundness * self.extension.scale,
            bottomleft_roundness=0,
            bottomright_roundness=0
        )
        # Right side panel
        self.fill_rounded_rect(
            self.extension.extend(self.screen_right, 150, ExtendMethod.LEFT),
            self.screen_bottom,
            self.screen_right,
            self.extension.extend(self.screen_bottom, 100, ExtendMethod.UP),
            color=self.side_panel_color,
            outline_thickness=self.panel_outline_thickness * self.extension.scale,
            outline_color=self.panel_outline_color,
            topleft_roundness=self.side_panel_roundness * self.extension.scale,
            topright_roundness=0,
            bottomleft_roundness=0,
            bottomright_roundness=0
        )
        # Bottom command panel
        self.fill_rect(
            self.extension.extend(self.screen_left, 150, ExtendMethod.RIGHT),
            self.screen_bottom,
            self.extension.extend(self.screen_right, 150, ExtendMethod.LEFT),
            self.extension.extend(self.screen_bottom, 80, ExtendMethod.UP),
            color=self.middle_panel_color,
            outline_thickness=self.panel_outline_thickness * self.extension.scale,
            outline_color=self.panel_outline_color
        )
        # Top menu panel
        self.fill_rect(
            self.screen_left,
            self.screen_top,
            self.screen_right,
            self.extension.extend(self.screen_top, 30, ExtendMethod.DOWN),
            color=self.middle_panel_color,
            outline_thickness=self.panel_outline_thickness * self.extension.scale,
            outline_color=self.panel_outline_color
        )

    def _draw_text(self):
        shadow_offset = self.title_text_shadow_offset * self.extension.scale
        title_x = self.screen_center_x
        title_y = self.extension.extend(self.screen_top, 15, ExtendMethod.DOWN)
        font = self.title_font.new_size(20 * self.extension.scale)
        anchor = Anchor.CENTER
        shadow_color = self.title_text_shadow_color
        # Above
        self.draw_text("Fleet Command", font, title_x, title_y - shadow_offset, anchor, shadow_color)
        # Below
        self.draw_text("Fleet Command", font, title_x, title_y + shadow_offset, anchor, shadow_color)
        # Left
        self.draw_text("Fleet Command", font, title_x - shadow_offset, title_y, anchor, shadow_color)
        # Right
        self.draw_text("Fleet Command", font, title_x + shadow_offset, title_y, anchor, shadow_color)
        # Title text (main)
        self.draw_text("Fleet Command", font, title_x, title_y, anchor, self.title_text_color)

    def _draw_team_info(self):
        team_font = self.context_font.new_size(14 * self.extension.scale)
        height_change = 20
        height_offset = 110
        for team in self.teams:
            team_units = [unit for unit in self.units if unit.team == team]
            self.draw_text(
                text=f"{team.name} - {len(team_units)}",
                font=team_font,
                x=self.extension.extend(self.screen_right, 75, ExtendMethod.LEFT),
                y=self.extension.extend(self.screen_bottom, height_offset, ExtendMethod.UP),
                anchor=Anchor.BOTTOM,
                color=team.color,
            )
            height_offset += height_change
