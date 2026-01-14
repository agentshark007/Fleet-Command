import core.asset as asset
import libraries.log as log
from libraries.pgiud import *


def initialize(self) -> None:
    log.info("Core initialization started")
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
    log.info("Core initialization complete")


def late_initialize(self) -> None:
    log.info("Core late initialization started")

    log.info("Core late initialization complete")


def load_assets(self) -> None:
    log.info(f"Loading assets started, with base path: {asset.BASE_PATH}")
    # Load fonts for UI text rendering
    self.title_font = Font(
        asset.asset("fonts/BlackOpsOne-Regular.ttf"), size=32
    )  # Large title font
    self.context_font = Font(
        asset.asset("fonts/WDXLLubrifontSC-Regular.ttf"), size=16
    )  # Regular UI font

    # Load images for world and UI rendering
    # Water texture for background
    self.water_image = Image(asset.asset("images/water.jpg"))
    self.selection_marker_image = Image(
        asset.asset("images/selection-marker.png")
    )  # Team color marker
    self.autonomous_target_image = Image(
        asset.asset("images/target.png")
    )  # Autonomous movement target
    self.projectile_images = [
        Image(asset.asset("images/projectile_0.png")),
        # Projectile images
        Image(asset.asset("images/projectile_1.png")),
        Image(asset.asset("images/projectile_2.png")),
    ]
    log.info("Loading assets complete")


def update(self) -> None:
    handle_gui_scaling(self)  # Handle GUI scale input


def late_update(self) -> None:
    # Store key state from this frame for next frame's input checks
    self.plus_last_frame = self.keydown(Key.EQUALS)  # Track if plus key was held
    self.minus_last_frame = self.keydown(Key.MINUS)  # Track if minus key was held
    # Track primary mouse button state
    self.mouseprimary_last_frame = self.mousedownprimary
    # Track middle mouse button state
    self.mousemiddle_last_frame = self.mousedownmiddle
    # Track secondary mouse button state
    self.mousesecondary_last_frame = self.mousedownsecondary
    self.space_last_frame = self.keydown(Key.SPACE)  # Track space key state


def handle_gui_scaling(self) -> None:
    # Detect if either command key (left or right) is held down
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

    # Only process +/- input when command key is held
    if command_down:
        # Scale up on plus key (only trigger once per key press)
        if self.keydown(Key.EQUALS) and not self.plus_last_frame:
            old_gui_scale = self.gui_scale
            self.gui_scale *= self.gui_scale_factor
            log.info(
                f"GUI scale increased: old={old_gui_scale}, new={
                    self.gui_scale}"
            )
        # Scale down on minus key (only trigger once per key press)
        elif self.keydown(Key.MINUS) and not self.minus_last_frame:
            old_gui_scale = self.gui_scale
            self.gui_scale /= self.gui_scale_factor
            log.info(
                f"GUI scale decreased: old={old_gui_scale}, new={
                    self.gui_scale}"
            )

    # Clamp GUI scale to valid range
    self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))


def draw(self) -> None:
    self.clear(Color(0, 0, 0))  # Clear screen to black


def late_draw(self) -> None:
    pass
