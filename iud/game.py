import math
from core.enums import GameState, ExtendDirection
from core.camera import Camera
from game.unit import *
from game.team import *
from panda2d import Key, Color, Anchor
from core.utility import distance

def initialize(self):
    initialize_settings(self)
    initialize_state_variables(self)
    initialize_game_logic(self)
    initialize_layout(self)


def initialize_settings(self):
    # Water
    self.water_state_speed = 5

    # Camera
    self.camera_zoom_speed = 0.1
    self.min_camera_scale = 0.3
    self.max_camera_scale = 3.0
    self.camera_move_speed = 50.0
    self.camera_move_friction = 0.9


    # Image scales
    self.selection_marker_scale = 0.03
    self.selection_distance = 100
    self.autonomous_target_image_scale = 0.05

    # Autonomous control
    self.target_stop_distance = 100
    self.autonomous_forward_backward_angle_threshold = 45

    # Selection marker offset
    self.selection_marker_offset = 20


def initialize_state_variables(self):
        # Game state
        self.game_state = GameState.MAINMENU

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


def initialize_game_logic(self):
        self.unit_types = [Battleship]

        team_count = 4
        self.teams = random_teams(team_count)
        self.units = [Battleship(team_index=random.randint(0, len(self.teams) - 1), position_x=random.uniform(-1000, 1000), position_y=random.uniform(-1000, 1000), direction=random.uniform(0, 360)) for _ in range(20)]


def initialize_layout(self):
        # GUI colors
        self.side_panel_color = Color(0, 0, 144, 150)
        self.middle_panel_color = Color(0, 0, 70, 150)
        self.panel_outline_color = Color(0, 0, 100, 50)
        self.title_text_color = Color(100, 100, 20)
        self.title_text_shadow_color = Color(20, 20, 50, 150)
        self.title_text_shadow_offset = 1

        # GUI shapes
        self.panel_outline_thickness = 2
        self.side_panel_roundness = 15

        # Game filters
        self.other_unit_filter = Color(150, 150, 150, 255)
        self.hover_unit_filter = Color(200, 200, 200, 255)
        self.selected_unit_filter = Color(255, 255, 255, 255)



def update(self):
    handle_camera_zoom_input(self)
    handle_unit_selection(self)
    handle_unit_control(self)
    handle_camera_movement(self)
    update_water(self)


def handle_camera_zoom_input(self):
        # Detect if either command key held down
        command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

        # Get -/+ input for camera zoom (only when command is NOT held)
        if not command_down:
            if self.keydown(Key.EQUALS) and not self.plus_last_frame:
                self.camera.scale = min([self.max_camera_scale, self.camera.scale + self.camera_zoom_speed])

            elif self.keydown(Key.MINUS) and not self.minus_last_frame:
                self.camera.scale = max([self.min_camera_scale, self.camera.scale - self.camera_zoom_speed])


def handle_unit_selection(self):
    """Select a unit under the cursor when clicking, restricted to player team."""
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

    # Handle selection input
    if self.mousedownprimary:
        if self.teams[self.units[closest_unit_index_selectable].team_index].type == TeamType.PLAYER: # Only allow selecting player team units
            self.selected_unit_index = closest_unit_index_selectable
        else:
            self.selected_unit_index = -1


def handle_unit_control(self):
    # Helper functions
    def manual_override():
        return any([
            self.keydown(Key.W),
            self.keydown(Key.S),
            self.keydown(Key.A),
            self.keydown(Key.D)
        ])

    # Get unit control input
    for index, unit in enumerate(self.units):
        if index == self.selected_unit_index:
            # Detect autonomous mode activation
            if self.mousedownsecondary:
                # Set autonomous target to mouse world position
                mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)
                unit.autonomous = True
                unit.autonomous_target_x = mouse_world_x
                unit.autonomous_target_y = mouse_world_y

            # Detect autonomous mode deactivation
            if manual_override():
                # Disable autonomous control on manual input
                unit.autonomous = False

            if unit.autonomous:
                # Accelerate and turn towards target

                # Calculate important values
                target_x, target_y = unit.autonomous_target_x, unit.autonomous_target_y
                dx = target_x - unit.position_x
                dy = target_y - unit.position_y
                distance_to_target = math.hypot(dx, dy)

                # Stop if target reached
                if distance_to_target < self.target_stop_distance:
                    # Stop if close to target and deactivate autonomous mode
                    unit.autonomous = False
                    continue

                # Calculate angle to target
                angle_to_target = math.degrees(math.atan2(dx, dy))

                # Calculate angle difference in range -180 to 180
                angle_diff = (angle_to_target - unit.direction + 360) % 360
                if angle_diff > 180:
                    angle_diff -= 360

                # Determine acceleration and rotation direction
                if abs(angle_diff) < self.autonomous_forward_backward_angle_threshold:
                    # If angle difference is less than 90 degrees, move forward
                    direction = max(-unit.rotation_speed, min(unit.rotation_speed, angle_diff))
                    acceleration = unit.speed
                else:
                    # If angle difference is more than 90 degrees, move backward
                    direction = max(-unit.rotation_speed, min(unit.rotation_speed, angle_diff))
                    acceleration = -unit.speed

                # Cap acceleration and rotation to make sure no bugs occor
                acceleration = min(acceleration, unit.speed)
                direction = max(-unit.rotation_speed, min(unit.rotation_speed, direction))

                unit.acceleration = acceleration
                unit.rotation_acceleration = direction
            else:
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

                # Cap acceleration and rotation to make sure no bugs occor
                acceleration = min(acceleration, unit.speed)
                direction = max(-unit.rotation_speed, min(unit.rotation_speed, direction))

                unit.acceleration = acceleration
                unit.rotation_acceleration = direction

        elif self.teams[unit.team_index].type == TeamType.PLAYER:
            pass # Do nothing for non-selected player units

        elif self.teams[unit.team_index].type == TeamType.AI:
            # Simple AI for units
            pass
    
    # Run physics and movement for all units
    for unit in self.units:
        # Update velocities based on acceleration
        angle_rad = math.radians(unit.direction)
        unit.velocity_x += math.sin(angle_rad) * unit.acceleration * self.deltatime
        unit.velocity_y += math.cos(angle_rad) * unit.acceleration * self.deltatime
        unit.velocity_rotation += unit.rotation_acceleration * self.deltatime

        # Apply friction
        unit.velocity_x *= unit.friction
        unit.velocity_y *= unit.friction
        unit.velocity_rotation *= unit.rotation_friction
        
        # Update position and direction
        unit.direction += unit.velocity_rotation * self.deltatime
        unit.position_x += unit.velocity_x * self.deltatime
        unit.position_y += unit.velocity_y * self.deltatime

        # Clear accelerations
        unit.acceleration = 0
        unit.rotation_acceleration = 0


def handle_camera_movement(self):
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


def update_water(self):
    self.water_state += self.water_state_speed * self.deltatime



def draw(self):
    draw_water(self)
    draw_units(self)


def draw_units(self):
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
                xscale=0.5 * self.camera.scale,
                yscale=0.5 * self.camera.scale,
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
                    xscale=self.autonomous_target_image_scale * self.camera.scale,
                    yscale=self.autonomous_target_image_scale * self.camera.scale,
                    rotation=0
                )
        elif index == closest_unit_index_selectable:
            # Hovered unit
            self.draw_image(
                unit.image,
                screen_x,
                screen_y,
                anchor=Anchor.CENTER,
                xscale=0.5 * self.camera.scale,
                yscale=0.5 * self.camera.scale,
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
                xscale=0.5 * self.camera.scale,
                yscale=0.5 * self.camera.scale,
                filter=self.other_unit_filter,
                rotation=unit.direction
            )

    # Draw unit team marker
    for index, unit in enumerate(self.units):
        # Calculate the screen position of the marker
        screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
        
        
        # Draw the marker
        self.draw_image(
            self.selection_marker_image,
            screen_x,
            screen_y + self.selection_marker_offset * self.camera.scale,
            anchor=Anchor.BOTTOM,
            xscale=self.selection_marker_scale * self.camera.scale,
            yscale=self.selection_marker_scale  * self.camera.scale,
            filter=self.teams[unit.team_index].color.color,
            rotation=0
        )


def draw_water(self):
        """Render parallax water layers with varied movement and alpha."""
        # Simulate water movement by offsetting the tiling based on water state and also moving other layers in different ways
        
        # Base layer, not moving
        draw_tiled_water(
            self,
            Color(170, 150, 150, 255),
            0.0,
            0.0
        )

        # Second layer, moving in one direction
        draw_tiled_water(
            self,
            Color(150, 170, 150, 200),
            self.water_state * -2,
            self.water_state * -2
        )

        # Third layer, moving in a circle
        draw_tiled_water(
            self,
            Color(150, 150, 170, 120),
            math.cos(self.water_state * 0.1) * 20.0,
            math.sin(self.water_state * 0.1) * 20.0
        )


def draw_tiled_water(self, filter_color: Color, offset_x: float = 0.0, offset_y: float = 0.0):
    offset = 5 # Pixels to overlap tiles by to avoid gaps

    # World-space tiling; no gaps; zoom centered
    world_tile_w = (self.water_image.get_width() - offset) * self.water_image_scale
    world_tile_h = (self.water_image.get_height() - offset) * self.water_image_scale

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

    xscale = self.water_image_scale * self.camera.scale
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

    # Fleet Command title
    shadow_offset = self.title_text_shadow_offset * self.gui_scale
    title_x = self.screen_center_x
    title_y = self.extend(self.screen_top, 15, ExtendDirection.DOWN)
    font = self.title_font.new_size(20 * self.gui_scale)
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
