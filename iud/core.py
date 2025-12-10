from panda2d import Font, Image, Key

def initialize(self):
    # GUI scale
    self.gui_scale_factor = 20.0
    self.gui_scale_offset = 1.0
    self.gui_scale_min = 0.3
    self.gui_scale_max = 5.0

    # Assets
    load_assets(self)

def late_initialize(self):
    pass

def load_assets(self):
        """Load fonts and images used by the game."""
        # Fonts
        self.title_font = Font("assets/fonts/BlackOpsOne-Regular.ttf", size=32)
        self.context_font = Font("assets/fonts/WDXLLubrifontSC-Regular.ttf", size=16)
        
        # Images
        self.water_image = Image("assets/images/water.jpg")
        self.water_image_scale = 0.3
        self.selection_marker_image = Image("assets/images/selection-marker.png")
        self.autonomous_target_image = Image("assets/images/target.png")



def update(self):
    handle_gui_scaling(self)

def late_update(self):
    self.plus_last_frame = self.keydown(Key.EQUALS)
    self.minus_last_frame = self.keydown(Key.MINUS)

def handle_gui_scaling(self):
    # Calculate gui scale growth
    growth = self.gui_scale_offset + self.gui_scale_factor * self.deltatime

    # Detect if either command key held down
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)

    # Get -/+ input for GUI scale (only when command is held)
    if command_down:
        if self.keydown(Key.EQUALS) and not self.plus_last_frame:
            self.gui_scale *= growth

        elif self.keydown(Key.MINUS) and not self.minus_last_frame:
            self.gui_scale /= growth

    # Clamp gui scale
    self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))



def draw(self):
    pass
