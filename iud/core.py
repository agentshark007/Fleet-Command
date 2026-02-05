from core import asset
from libraries import log
from libraries.pgiud import *

def initialize(self) -> None:
    log.info('Core initialization started')
    self.gui_scale_factor = 1.3
    self.gui_scale_min = 0.3
    self.gui_scale_max = 5.0
    load_assets(self)
    self.plus_last_frame = False
    self.minus_last_frame = False
    self.mouse_primary_last_frame = False
    self.mouse_middle_last_frame = False
    self.mouse_secondary_last_frame = False
    self.mouse_last_frame = V(0, 0)
    log.info('Core initialization complete')

def late_initialize(self) -> None:
    log.info('Core late initialization started')
    log.info('Core late initialization complete')

def load_assets(self) -> None:
    log.info(f'Loading assets started, with base path: {asset.BASE_PATH}')
    self.title_font = Font(asset.asset('fonts/BlackOpsOne-Regular.ttf'), size=32)
    self.context_font = Font(asset.asset('fonts/WDXLLubrifontSC-Regular.ttf'), size=16)
    self.water_image = Image(asset.asset('images/water.jpg'))
    self.selection_marker_image = Image(asset.asset('images/selection-marker.png'))
    self.autonomous_target_image = Image(asset.asset('images/target.png'))
    self.projectile_images = [Image(asset.asset('images/projectile/projectile_0.png')), Image(asset.asset('images/projectile/projectile_1.png')), Image(asset.asset('images/projectile/projectile_2.png'))]
    log.info('Loading assets complete')

def update(self) -> None:
    handle_gui_scaling(self)

def late_update(self) -> None:
    self.plus_last_frame = self.keydown(Key.EQUALS)
    self.minus_last_frame = self.keydown(Key.MINUS)
    self.mouse_primary_last_frame = self.mouse_down_primary
    self.mouse_middle_last_frame = self.mouse_down_middle
    self.mouse_secondary_last_frame = self.mouse_down_secondary
    self.mouse_last_frame = self.mouse_pos

def handle_gui_scaling(self) -> None:
    command_down = self.keydown(Key.LSUPER) or self.keydown(Key.RSUPER)
    if command_down:
        if self.keydown(Key.EQUALS) and (not self.plus_last_frame):
            old_gui_scale = self.gui_scale
            self.gui_scale *= self.gui_scale_factor
            log.info(f'GUI scale increased: old={old_gui_scale}, new={self.gui_scale}')
        elif self.keydown(Key.MINUS) and (not self.minus_last_frame):
            old_gui_scale = self.gui_scale
            self.gui_scale /= self.gui_scale_factor
            log.info(f'GUI scale decreased: old={old_gui_scale}, new={self.gui_scale}')
    self.gui_scale = max(self.gui_scale_min, min(self.gui_scale, self.gui_scale_max))

def draw(self) -> None:
    self.clear(Color(0, 0, 0))

def late_draw(self) -> None:
    pass
