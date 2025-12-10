"""Main game state module for Fleet Command.

This module handles all gameplay logic including initialization, unit control,
camera management, unit rendering, water rendering, and UI panels. It manages
the core game loop while a player is actively playing.
"""

import math
from core.enums import GameState, ExtendDirection
from core.camera import Camera
from game.unit import *
from game.team import *
from panda2d import Key, Color, Anchor
from core.utility import distance

def initialize(self):
    """Initialize all gameplay systems and game state.
    
    Sets up settings, state variables, game logic, and UI layout.
    """
    initialize_settings(self)  # Load configuration values
    initialize_state_variables(self)  # Initialize variables
    initialize_game_logic(self)  # Create teams and units
    initialize_layout(self)  # Set up UI colors and appearance


def initialize_settings(self):
    """Load and configure game settings.
    
    Sets up parameters for water animation, camera, image scaling,
    autonomous unit behavior, and UI markers.
    """
    # Water animation
    self.water_state_speed = 5  # Speed of water animation cycles

    # Camera controls
    self.camera_zoom_speed = 0.1  # Rate of zoom change per frame
    self.min_camera_scale = 0.3  # Minimum zoom level
    self.max_camera_scale = 3.0  # Maximum zoom level
    self.camera_move_speed = 50.0  # Pixels per second for camera movement
    self.camera_move_friction = 0.9  # Friction for smooth camera deceleration

    # Visual scaling
    self.selection_marker_scale = 0.03  # Scale of unit team markers
    self.selection_distance = 100  # Pixels: range for selecting units
    self.autonomous_target_image_scale = 0.05  # Scale of autonomous target indicators

    # Autonomous movement
    self.target_stop_distance = 100  # Distance to stop at target
    self.autonomous_forward_backward_angle_threshold = 45  # Degrees: threshold for moving backward

    # UI positioning
    self.selection_marker_offset = 20  # Pixels above unit for team marker


def initialize_state_variables(self):
    """Initialize game state variables.
    
    Sets up the current game state, camera, unit selection, and animation counters.
    """
    # GUI scaling key state tracking
    self.plus_last_frame = False  # Track if plus key was held last frame (prevent repeat)
    self.minus_last_frame = False  # Track if minus key was held last frame (prevent repeat)
    self.gui_scale = 1.0  # Current GUI scale multiplier

    # Water animation
    self.water_state = 0  # Current animation frame counter for water

    # Camera
    self.camera = Camera(0.0, 0.0, 1.0)  # Create camera at origin with default zoom

    # Selection
    self.selected_units_index = []  # List of selected unit indices


def initialize_game_logic(self):
    """Initialize game logic including teams and units.
    
    Creates random teams and spawns initial units on the map.
    """
    # Available unit types that can be created
    self.unit_types = [Battleship]

    # Generate random teams for this game session
    team_count = 4
    self.teams = random_teams(team_count)
    
    # Create initial battleships for each team with random positions and rotations
    self.units = [
        Battleship(
            team_index=random.randint(0, len(self.teams) - 1),
            position_x=random.uniform(-1000, 1000),
            position_y=random.uniform(-1000, 1000),
            direction=random.uniform(0, 360)
        ) for _ in range(20)  # Spawn 20 units total
    ]


def initialize_layout(self):
    """Initialize UI visual settings and colors.
    
    Sets up all colors and styling for panels, text, and unit filters.
    """
    # GUI panel colors
    self.side_panel_color = Color(0, 0, 144, 150)  # Side panel background color
    self.middle_panel_color = Color(0, 0, 70, 150)  # Middle panel color
    self.panel_outline_color = Color(0, 0, 100, 50)  # Panel border color
    self.title_text_color = Color(100, 100, 20)  # Title text color
    self.title_text_shadow_color = Color(20, 20, 50, 150)  # Title shadow color
    self.title_text_shadow_offset = 1  # Pixels of shadow offset

    # GUI shape properties
    self.panel_outline_thickness = 2  # Pixels: panel border width
    self.side_panel_roundness = 15  # Pixels: corner roundness for side panels

    # Unit visual filters (color tints applied when rendering)
    self.other_unit_filter = Color(150, 150, 150, 255)  # Neutral units
    self.hover_unit_filter = Color(200, 200, 200, 255)  # Hovered units
    self.selected_unit_filter = Color(255, 255, 255, 255)  # Selected units (bright white)



def update(self):
    """Update the game state every frame.
    
    Handles camera input, unit selection, unit control, and camera movement.
    Called once per frame during active gameplay.
    """
    handle_camera_zoom_input(self)  # Process camera zoom keys
    handle_unit_selection(self)  # Handle unit selection clicks
    handle_unit_control(self)  # Process unit movement and physics
    handle_camera_movement(self)  # Process camera movement
    update_water(self)  # Advance water animation


def handle_camera_zoom_input(self):
    """Handle camera zoom input from keyboard.
    
    Allows the user to zoom the camera in and out using Plus/Minus keys
    (when Command is NOT held). Command+Plus/Minus is reserved for GUI scaling.
    """
    # Detect if either command key is held down
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

    # Get +/- input for camera zoom (only when command is NOT held)
    if not command_down:
        # Zoom in when plus key pressed
        if self.keydown(Key.EQUALS) and not self.plus_last_frame:
            self.camera.scale = min([self.max_camera_scale, self.camera.scale + self.camera_zoom_speed])

        # Zoom out when minus key pressed
        elif self.keydown(Key.MINUS) and not self.minus_last_frame:
            self.camera.scale = max([self.min_camera_scale, self.camera.scale - self.camera_zoom_speed])


def handle_unit_selection(self):
    """Select a unit under the cursor when clicking.
    
    Restricts selection to player-controlled team units. Updates the selected
    unit index based on the closest unit within the selection distance.
    """
    # Calculate mouse position in world coordinates (using camera)
    mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)
    
    # Find the closest unit and closest selectable unit to the mouse
    closest_unit_index = -1
    closest_unit_index_selectable = -1
    closest_distance = float('inf')
    closest_distance_selectable = float('inf')
    
    for index, unit in enumerate(self.units):
        dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
        # Track closest unit overall
        if dist < closest_distance:
            closest_distance = dist
            closest_unit_index = index
        # Track closest unit within selection range
        if dist < closest_distance_selectable and dist < self.selection_distance:
            closest_distance_selectable = dist
            closest_unit_index_selectable = index

    # Handle selection input (left mouse button)
    if self.mousedownprimary:
        # Only allow selecting units from the player team
        if closest_unit_index_selectable != -1 and self.teams[self.units[closest_unit_index_selectable].team_index].type == TeamType.PLAYER:
            if self.keydown(Key.LSHIFT) or self.keydown(Key.RSHIFT):
                self.selected_units_index.append(closest_unit_index_selectable)
            else:
                self.selected_units_index = [closest_unit_index_selectable]
        else:
            self.selected_units_index = []


def handle_unit_control(self):
    """Process unit movement input and update unit physics.
    
    Handles player input for manual control, autonomous target setting,
    physics calculations, and AI behavior (placeholder).
    """
    # Helper function to check if any manual control keys are held
    def manual_override():
        """Check if any movement keys (W/A/S/D) are pressed."""
        return any([
            self.keydown(Key.W),  # Forward
            self.keydown(Key.S),  # Backward
            self.keydown(Key.A),  # Left turn
            self.keydown(Key.D)   # Right turn
        ])

    # Process input and control for all units
    for index, unit in enumerate(self.units):
        # Handle input for selected unit only
        if index in self.selected_units_index:
            # Right-click sets autonomous target
            if self.mousedownsecondary:
                mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)
                unit.autonomous = True
                unit.autonomous_target_x = mouse_world_x
                unit.autonomous_target_y = mouse_world_y
            # Manual key input overrides autonomous movement
            if manual_override():
                unit.autonomous = False

        # Autonomous movement for units with autonomous=True
        if unit.autonomous:
            # Calculate direction and distance to target
            target_x, target_y = unit.autonomous_target_x, unit.autonomous_target_y
            dx = target_x - unit.position_x
            dy = target_y - unit.position_y
            distance_to_target = math.hypot(dx, dy)
            
            # Stop moving if we've reached the target
            if distance_to_target < self.target_stop_distance:
                unit.autonomous = False
                continue
            
            # Calculate angle to target
            angle_to_target = math.degrees(math.atan2(dx, dy))
            angle_diff = (angle_to_target - unit.direction + 360) % 360
            if angle_diff > 180:
                angle_diff -= 360
            
            # Decide movement direction based on angle
            if abs(angle_diff) < self.autonomous_forward_backward_angle_threshold:
                # Face target and move forward
                direction = max(-unit.rotation_speed, min(unit.rotation_speed, angle_diff))
                acceleration = unit.speed
            else:
                # Move backward while turning (faster evasion)
                direction = max(-unit.rotation_speed, min(unit.rotation_speed, angle_diff))
                acceleration = -unit.speed
            
            # Clamp accelerations to valid ranges
            acceleration = min(acceleration, unit.speed)
            direction = max(-unit.rotation_speed, min(unit.rotation_speed, direction))
            unit.acceleration = acceleration
            unit.rotation_acceleration = direction
            
        elif index in self.selected_units_index:
            # Manual control for selected unit (only if not autonomous)
            acceleration = 0
            direction = 0
            
            # Process movement input
            if self.keydown(Key.W):
                acceleration += unit.speed  # Move forward
            if self.keydown(Key.S):
                acceleration -= unit.speed  # Move backward
            # Only allow turning when moving (to prevent spinning in place)
            if self.keydown(Key.A) and acceleration != 0:
                direction -= unit.rotation_speed  # Turn left
            if self.keydown(Key.D) and acceleration != 0:
                direction += unit.rotation_speed  # Turn right
            
            # Clamp accelerations to valid ranges
            acceleration = min(acceleration, unit.speed)
            direction = max(-unit.rotation_speed, min(unit.rotation_speed, direction))
            unit.acceleration = acceleration
            unit.rotation_acceleration = direction
            
        elif self.teams[unit.team_index].type == TeamType.PLAYER:
            # Non-selected player units: idle (no input)
            pass
        elif self.teams[unit.team_index].type == TeamType.AI:
            # AI-controlled units: placeholder for future AI logic
            pass
    
    # Run physics and movement for all units
    for unit in self.units:
        # Calculate velocity changes from acceleration
        angle_rad = math.radians(unit.direction)
        unit.velocity_x += math.sin(angle_rad) * unit.acceleration * self.deltatime
        unit.velocity_y += math.cos(angle_rad) * unit.acceleration * self.deltatime
        unit.velocity_rotation += unit.rotation_acceleration * self.deltatime

        # Apply friction to velocities (exponential decay - frame-independent)
        # friction^(deltatime / frame_time) where frame_time=1/60 for 60 FPS
        friction_factor = pow(unit.friction, self.deltatime * 60)
        unit.velocity_x *= friction_factor
        unit.velocity_y *= friction_factor
        rotation_friction_factor = pow(unit.rotation_friction, self.deltatime * 60)
        unit.velocity_rotation *= rotation_friction_factor
        
        # Update position and rotation based on velocities
        unit.direction += unit.velocity_rotation * self.deltatime
        unit.position_x += unit.velocity_x * self.deltatime
        unit.position_y += unit.velocity_y * self.deltatime

        # Reset accelerations for next frame
        unit.acceleration = 0
        unit.rotation_acceleration = 0


def handle_camera_movement(self):
    """Handle camera movement input from arrow keys.
    
    Allows smooth camera panning using arrow keys with friction-based deceleration.
    """
    # Accelerate camera based on arrow key input
    if self.keydown(Key.LEFT):
        self.camera.velocity_x -= self.camera_move_speed * self.deltatime  # Move camera left
    if self.keydown(Key.RIGHT):
        self.camera.velocity_x += self.camera_move_speed * self.deltatime  # Move camera right
    if self.keydown(Key.UP):
        self.camera.velocity_y += self.camera_move_speed * self.deltatime  # Move camera up
    if self.keydown(Key.DOWN):
        self.camera.velocity_y -= self.camera_move_speed * self.deltatime  # Move camera down

    # Apply friction to camera velocity (smooth deceleration - frame-independent)
    friction_factor = pow(self.camera_move_friction, self.deltatime * 60)
    self.camera.velocity_x *= friction_factor
    self.camera.velocity_y *= friction_factor

    # Update camera position based on velocity
    self.camera.x += self.camera.velocity_x
    self.camera.y += self.camera.velocity_y


def update_water(self):
    """Update water animation state.
    
    Increments the water state counter which drives the parallax animation.
    """
    self.water_state += self.water_state_speed * self.deltatime



def draw(self):
    """Render the current game frame.
    
    Draws water background, units, and UI panels in the correct order.
    """
    draw_water(self)  # Draw water background
    draw_units(self)  # Draw all units
    draw_ui_panels(self)  # Draw UI panels and title


def draw_units(self):
    """Render all units with appropriate visual effects and markers.
    
    Draws units with different colors based on selection state (selected, hovered, or normal).
    Also renders selection markers showing team color and autonomous targets for selected units.
    """
    # Calculate mouse position in world coordinates for hover detection
    mouse_world_x, mouse_world_y = self.camera.deduce(self.mousex, self.mousey)

    # Find closest unit to mouse for hover effect
    closest_unit_index = -1
    closest_unit_index_selectable = -1
    closest_distance = float('inf')
    closest_distance_selectable = float('inf')
    
    for index, unit in enumerate(self.units):
        dist = distance(unit.position_x, unit.position_y, mouse_world_x, mouse_world_y)
        # Track closest unit overall
        if dist < closest_distance:
            closest_distance = dist
            closest_unit_index = index
        # Track closest unit within selection range
        if dist < closest_distance_selectable and dist < self.selection_distance:
            closest_distance_selectable = dist
            closest_unit_index_selectable = index

    # Render all units with appropriate colors
    for index, unit in enumerate(self.units):
        # Project unit world position to screen coordinates
        screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
        
        # Draw unit image with color based on state
        if index in self.selected_units_index:
            # Selected unit: bright white highlight
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

            # Draw autonomous target indicator if moving autonomously
            if unit.autonomous:
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
            # Hovered unit: lighter highlight to indicate it's selectable
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
            # Other units: neutral gray color
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

    # Draw team color markers above each unit
    for index, unit in enumerate(self.units):
        # Project unit position to screen coordinates
        screen_x, screen_y = self.camera.project(unit.position_x, unit.position_y)
        
        # Draw colored marker above unit showing team color
        self.draw_image(
            self.selection_marker_image,
            screen_x,
            screen_y + self.selection_marker_offset * self.camera.scale,
            anchor=Anchor.BOTTOM,
            xscale=self.selection_marker_scale * self.camera.scale,
            yscale=self.selection_marker_scale * self.camera.scale,
            filter=self.teams[unit.team_index].color.color,
            rotation=0
        )


def draw_water(self):
    """Render parallax water layers with varied movement and alpha transparency.
    
    Creates a layered water effect using three animated tiles moving at different
    speeds and with different opacity levels for visual depth.
    """
    # Base layer: stationary
    draw_tiled_water(
        self,
        Color(170, 150, 150, 255),  # Brownish base layer
        0.0,  # No horizontal offset
        0.0   # No vertical offset
    )

    # Second layer: moving diagonally
    draw_tiled_water(
        self,
        Color(150, 170, 150, 200),  # Greenish layer with transparency
        self.water_state * -2,  # Move left
        self.water_state * -2   # Move down
    )

    # Third layer: moving in circle pattern
    draw_tiled_water(
        self,
        Color(150, 150, 170, 120),  # Blueish layer with high transparency
        math.cos(self.water_state * 0.1) * 20.0,  # Circular X offset
        math.sin(self.water_state * 0.1) * 20.0   # Circular Y offset
    )


def draw_tiled_water(self, filter_color: Color, offset_x: float = 0.0, offset_y: float = 0.0):
    """Render a tiled water layer at a given offset.
    
    Uses world-space tiling to ensure smooth parallax scrolling without gaps
    as the camera moves. The camera position is factored with the offset to
    create the parallax effect.
    
    Args:
        filter_color: Color to tint the water tiles with (includes alpha).
        offset_x: Horizontal offset for this layer's animation.
        offset_y: Vertical offset for this layer's animation.
    """
    # Small overlap to prevent gaps between tiles
    offset = 5

    # Calculate tile dimensions in world space
    world_tile_w = (self.water_image.get_width() - offset) * self.water_image_scale
    world_tile_h = (self.water_image.get_height() - offset) * self.water_image_scale

    # Get screen dimensions
    screen_w = self.screen_right - self.screen_left
    screen_h = self.screen_top - self.screen_bottom

    # Effective camera position with offsets (creates parallax effect)
    eff_cam_x = self.camera.x + offset_x
    eff_cam_y = self.camera.y + offset_y

    # Convert screen edges to world coordinates using effective camera
    world_left = self.screen_left / self.camera.scale + eff_cam_x
    world_bottom = self.screen_bottom / self.camera.scale + eff_cam_y
    world_right = self.screen_right / self.camera.scale + eff_cam_x
    world_top = self.screen_top / self.camera.scale + eff_cam_y

    # Calculate starting position for tiling (align to grid)
    start_world_x = world_left - (world_left % world_tile_w) - world_tile_w
    start_world_y = world_bottom - (world_bottom % world_tile_h) - world_tile_h

    # Calculate screen-space tile dimensions
    tile_w_screen = world_tile_w * self.camera.scale
    tile_h_screen = world_tile_h * self.camera.scale
    
    # Calculate how many tiles needed to cover screen
    cols = int(math.ceil(screen_w / tile_w_screen)) + 3
    rows = int(math.ceil(screen_h / tile_h_screen)) + 3

    # Calculate scale factors for rendering
    xscale = self.water_image_scale * self.camera.scale
    yscale = xscale

    # Render all tiles
    for col in range(cols):
        for row in range(rows):
            # Calculate world position of this tile
            wx = start_world_x + col * world_tile_w
            wy = start_world_y + row * world_tile_h
            # Project to screen space (subtract offsets to undo parallax for rendering)
            sx, sy = self.camera.project(wx - offset_x, wy - offset_y)
            # Draw the tile
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


def draw_ui_panels(self):
    """Render all UI panels and title text.
    
    Draws the side panels, bottom command panel, top menu panel, and
    "Fleet Command" title with shadow effect.
    """
    # Left side panel (with rounded corner)
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
    
    # Right side panel (with rounded corner)
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
    
    # Bottom command panel (between side panels)
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

    # Draw "Fleet Command" title with shadow effect
    shadow_offset = self.title_text_shadow_offset * self.gui_scale
    title_x = self.screen_center_x
    title_y = self.extend(self.screen_top, 15, ExtendDirection.DOWN)
    font = self.title_font.new_size(20 * self.gui_scale)
    anchor = Anchor.CENTER
    shadow_color = self.title_text_shadow_color
    
    # Draw shadow in four directions for depth effect
    # Above
    self.draw_text("Fleet Command", font, title_x, title_y - shadow_offset, anchor, shadow_color)
    # Below
    self.draw_text("Fleet Command", font, title_x, title_y + shadow_offset, anchor, shadow_color)
    # Left
    self.draw_text("Fleet Command", font, title_x - shadow_offset, title_y, anchor, shadow_color)
    # Right
    self.draw_text("Fleet Command", font, title_x + shadow_offset, title_y, anchor, shadow_color)

    # Draw title text main (bright color on top of shadow)
    self.draw_text("Fleet Command", font, title_x, title_y, anchor, self.title_text_color)
