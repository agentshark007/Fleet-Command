from core.asset import asset
from core.enums import ExtendDirection, GameState
from core.utility import mouse_in_area
from libraries import log
from libraries.pgiud import *


def initialize(self) -> None:
    log.info("Main menu initialization started")
    self.mainmenu_button_extend_x = 50
    self.mainmenu_button_extend_y = 50
    self.mainmenu_button_spacing = 20
    self.mainmenu_button_width = 150
    self.mainmenu_button_height = 60
    self.mainmenu_button_roundness = 15
    self.mainmenu_background_color = Color(0, 0, 50)
    self.mainmenu_button_color = Color(0, 0, 100)
    self.mainmenu_button_color_hover = Color(30, 30, 130)
    self.mainmenu_button_outline_thickness = 2
    self.mainmenu_button_outline_color = Color(0, 0, 0)
    self.music = Sound(asset("sounds/cinematic-powerful-battle-music-414692.mp3"))
    self.music_started = False
    log.info("Main menu initialized")


def update(self) -> None:
    if not self.music_started:
        if self.menu_state == GameState.MAINMENU:
            self.music.play()
            self.music_started = True
    buttons = [("newgame", newgame), ("settings", settings), ("quit", _quit)]
    for index, (button_id, action) in enumerate(reversed(buttons)):
        left, bottom, right, top = get_button_bounds(self, index)
        if mouse_in_area(*self.mouse_pos.to_tuple(), left, right, bottom, top):
            if self.mousedownprimary:
                action(self)
                log.info(f"Main menu button clicked: id={button_id}")
                break


def newgame(self) -> None:
    self.menu_state = GameState.GAME
    self.music.stop()


def settings(self) -> None:
    self.menu_state = GameState.SETTINGS


def _quit(self) -> None:
    self._running = False
    self.music.stop()
    log.info("Quit action triggered from main menu")


def draw(self) -> None:
    self.fill_rect(
        V(self.screen_left, self.screen_bottom),
        V(self.screen_right, self.screen_top),
        color=self.mainmenu_background_color,
    )
    buttons = [("newgame", "New Game"), ("settings", "Settings"), ("quit", "Quit")]
    for index, (button_id, button_text) in enumerate(buttons):
        draw_button(self, button_text, index, len(buttons))


def get_button_bounds(self, index: int) -> tuple[float, float, float, float]:
    button_left = self.extend(
        self.screen_left, self.mainmenu_button_extend_x, ExtendDirection.RIGHT
    )
    button_bottom = self.extend(
        self.screen_bottom, self.mainmenu_button_extend_y, ExtendDirection.UP
    )
    button_right = self.extend(
        button_left, self.mainmenu_button_width, ExtendDirection.RIGHT
    )
    button_top = self.extend(
        button_bottom, self.mainmenu_button_height, ExtendDirection.UP
    )
    spacing = (
        self.mainmenu_button_spacing + self.mainmenu_button_height
    ) * self.gui_scale
    vertical_offset = spacing * index
    left = button_left
    bottom = button_bottom + vertical_offset
    right = button_right
    top = button_top + vertical_offset
    return (left, bottom, right, top)


def draw_button(self, text, index, max_index):
    left, bottom, right, top = get_button_bounds(self, max_index - index - 1)
    button_color = (
        self.mainmenu_button_color_hover
        if mouse_in_area(*self.mouse_pos.to_tuple(), left, right, bottom, top)
        else self.mainmenu_button_color
    )
    self.fill_rounded_rect(
        V(left, bottom),
        V(right, top),
        color=button_color,
        outline_thickness=self.mainmenu_button_outline_thickness * self.gui_scale,
        outline_color=self.mainmenu_button_outline_color,
        topleft_roundness=self.mainmenu_button_roundness * self.gui_scale,
        topright_roundness=self.mainmenu_button_roundness * self.gui_scale,
        bottomleft_roundness=self.mainmenu_button_roundness * self.gui_scale,
        bottomright_roundness=self.mainmenu_button_roundness * self.gui_scale,
    )
    self.draw_text(
        text,
        pos=V((left + right) / 2, (bottom + top) / 2),
        font=self.context_font.new_size(int(20 * self.gui_scale)),
        color=Color(255, 255, 255),
        origin=Origin.CENTER,
    )
