"""Core game systems module for Fleet Command.

This module handles initialization of core game systems including asset loading,
GUI scaling, and per-frame core updates.
"""

from panda2d import Font, Image, Key

def initialize(self):
    """Initialize core game systems.
    
    Sets up GUI scaling parameters and loads all game assets (fonts, images).
    """
    # GUI scaling configuration
    self.gui_scale_factor = 20.0  # Scaling factor for GUI (pixels per second)
    self.gui_scale_offset = 1.0  # Base multiplier for GUI scale changes
    self.gui_scale_min = 0.3  # Minimum allowed GUI scale
    self.gui_scale_max = 5.0  # Maximum allowed GUI scale

    # Load all game assets
    load_assets(self)

def late_initialize(self):
    """Late initialization step for core systems (currently unused)."""
    pass

def load_assets(self):
    """Load and cache all fonts and images used by the game.
    
    This function initializes Font and Image objects and stores them as
    instance variables for use throughout the game.
    """
    # Load fonts for UI text rendering
    self.title_font = Font("assets/fonts/BlackOpsOne-Regular.ttf", size=32)  # Large title font
    self.context_font = Font("assets/fonts/WDXLLubrifontSC-Regular.ttf", size=16)  # Regular UI font
    
    # Load images for world and UI rendering
    self.water_image = Image("assets/images/water.jpg")  # Water texture for background
    self.water_image_scale = 0.3  # Scale factor for water tiles
    self.selection_marker_image = Image("assets/images/selection-marker.png")  # Team color marker
    self.autonomous_target_image = Image("assets/images/target.png")  # Autonomous movement target



def update(self):
    """Update core systems (called every frame)."""
    handle_gui_scaling(self)  # Handle GUI scale input

def late_update(self):
    """Late update for core systems (called after all other updates).
    
    Tracks key states from this frame for use in next frame's input detection.
    """
    # Store key state from this frame for next frame's input checks
    self.plus_last_frame = self.keydown(Key.EQUALS)  # Track if plus key was held
    self.minus_last_frame = self.keydown(Key.MINUS)  # Track if minus key was held

def handle_gui_scaling(self):
    """Handle user input for adjusting GUI scale.
    
    Allows the user to zoom the UI in and out using Command+Plus/Minus keys.
    The scale is clamped between min and max values.
    """
    # Calculate growth rate based on delta time
    growth = self.gui_scale_offset + self.gui_scale_factor * self.deltatime

    # Detect if either command key (left or right) is held down
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

    # Only process +/- input when command key is held
    if command_down:
        # Scale up on plus key (only trigger once per key press)
        if self.keydown(Key.EQUALS) and not self.plus_last_frame:
            self.gui_scale *= growth
        # Scale down on minus key (only trigger once per key press)
        elif self.keydown(Key.MINUS) and not self.minus_last_frame:
            self.gui_scale /= growth

    # Clamp GUI scale to valid range
    self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))



def draw(self):
    """Draw core systems (currently unused)."""
    pass
