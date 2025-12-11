

from panda2d import Font, Image, Key, Color

def initialize(self) -> None:
    # GUI scaling configuration
    self.gui_scale_factor = 1.3  # Scaling factor for GUI (zoom in/out)
    self.gui_scale_min = 0.3  # Minimum allowed GUI scale
    self.gui_scale_max = 5.0  # Maximum allowed GUI scale

    # Load all game assets
    load_assets(self)

    # Reset key state tracking variables
    self.plus_last_frame = False  # Track plus key state
    self.minus_last_frame = False  # Track minus key state
    self.mouseprimary_last_frame = False  # Track primary mouse button state
    self.mousemiddle_last_frame = False  # Track middle mouse button state
    self.mousesecondary_last_frame = False  # Track secondary mouse button state
    self.space_last_frame = False  # Track space key state

def late_initialize(self) -> None:
    pass

def load_assets(self) -> None:
    # Load fonts for UI text rendering
    self.title_font = Font("assets/fonts/BlackOpsOne-Regular.ttf", size=32)  # Large title font
    self.context_font = Font("assets/fonts/WDXLLubrifontSC-Regular.ttf", size=16)  # Regular UI font
    
    # Load images for world and UI rendering
    self.water_image = Image("assets/images/water.jpg")  # Water texture for background
    self.selection_marker_image = Image("assets/images/selection-marker.png")  # Team color marker
    self.autonomous_target_image = Image("assets/images/target.png")  # Autonomous movement target
    self.projectile_images = [Image("assets/images/projectile_0.png"), Image("assets/images/projectile_1.png"), Image("assets/images/projectile_2.png")]  # Projectile images



def update(self) -> None:
    handle_gui_scaling(self)  # Handle GUI scale input

def late_update(self) -> None:
    # Store key state from this frame for next frame's input checks
    self.plus_last_frame = self.keydown(Key.EQUALS)  # Track if plus key was held
    self.minus_last_frame = self.keydown(Key.MINUS)  # Track if minus key was held
    self.mouseprimary_last_frame = self.mousedownprimary  # Track primary mouse button state
    self.mousemiddle_last_frame = self.mousedownmiddle  # Track middle mouse button state
    self.mousesecondary_last_frame = self.mousedownsecondary  # Track secondary mouse button state
    self.space_last_frame = self.keydown(Key.SPACE)  # Track space key state

def handle_gui_scaling(self) -> None:

    # Detect if either command key (left or right) is held down
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

    # Only process +/- input when command key is held
    if command_down:
        # Scale up on plus key (only trigger once per key press)
        if self.keydown(Key.EQUALS) and not self.plus_last_frame:
            self.gui_scale *= self.gui_scale_factor
        # Scale down on minus key (only trigger once per key press)
        elif self.keydown(Key.MINUS) and not self.minus_last_frame:
            self.gui_scale /= self.gui_scale_factor

    # Clamp GUI scale to valid range
    self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))



def draw(self) -> None:
    self.clear(Color(0, 0, 0))  # Clear screen to black

def late_draw(self) -> None:
    pass
