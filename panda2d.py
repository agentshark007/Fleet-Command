
# =============================
# Panda2D Framework - Core Classes
# =============================

import pygame
from enum import Enum
import math

###########################################################
# Key Enum
###########################################################

class Key(Enum):
    # Letters
    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    X = pygame.K_x
    Y = pygame.K_y
    Z = pygame.K_z

    # Numbers
    NUM_0 = pygame.K_0
    NUM_1 = pygame.K_1
    NUM_2 = pygame.K_2
    NUM_3 = pygame.K_3
    NUM_4 = pygame.K_4
    NUM_5 = pygame.K_5
    NUM_6 = pygame.K_6
    NUM_7 = pygame.K_7
    NUM_8 = pygame.K_8
    NUM_9 = pygame.K_9

    # Function keys
    F1 = pygame.K_F1
    F2 = pygame.K_F2
    F3 = pygame.K_F3
    F4 = pygame.K_F4
    F5 = pygame.K_F5
    F6 = pygame.K_F6
    F7 = pygame.K_F7
    F8 = pygame.K_F8
    F9 = pygame.K_F9
    F10 = pygame.K_F10
    F11 = pygame.K_F11
    F12 = pygame.K_F12

    # Arrows
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN

    # Modifiers
    LSHIFT = pygame.K_LSHIFT
    RSHIFT = pygame.K_RSHIFT
    LCTRL = pygame.K_LCTRL
    RCTRL = pygame.K_RCTRL
    LALT = pygame.K_LALT
    RALT = pygame.K_RALT
    LSUPER = pygame.K_LSUPER
    RSUPER = pygame.K_RSUPER

    # Common keys
    SPACE = pygame.K_SPACE
    RETURN = pygame.K_RETURN
    ENTER = pygame.K_RETURN
    ESCAPE = pygame.K_ESCAPE
    TAB = pygame.K_TAB
    BACKSPACE = pygame.K_BACKSPACE
    CAPSLOCK = pygame.K_CAPSLOCK
    INSERT = pygame.K_INSERT
    DELETE = pygame.K_DELETE
    HOME = pygame.K_HOME
    END = pygame.K_END
    PAGEUP = pygame.K_PAGEUP
    PAGEDOWN = pygame.K_PAGEDOWN

    # Symbols
    MINUS = pygame.K_MINUS
    EQUALS = pygame.K_EQUALS
    LEFTBRACKET = pygame.K_LEFTBRACKET
    RIGHTBRACKET = pygame.K_RIGHTBRACKET
    BACKSLASH = pygame.K_BACKSLASH
    SEMICOLON = pygame.K_SEMICOLON
    APOSTROPHE = pygame.K_QUOTE
    GRAVE = pygame.K_BACKQUOTE
    COMMA = pygame.K_COMMA
    PERIOD = pygame.K_PERIOD
    SLASH = pygame.K_SLASH

    # Keypad
    KP0 = pygame.K_KP0
    KP1 = pygame.K_KP1
    KP2 = pygame.K_KP2
    KP3 = pygame.K_KP3
    KP4 = pygame.K_KP4
    KP5 = pygame.K_KP5
    KP6 = pygame.K_KP6
    KP7 = pygame.K_KP7
    KP8 = pygame.K_KP8
    KP9 = pygame.K_KP9
    KP_PERIOD = pygame.K_KP_PERIOD
    KP_DIVIDE = pygame.K_KP_DIVIDE
    KP_MULTIPLY = pygame.K_KP_MULTIPLY
    KP_MINUS = pygame.K_KP_MINUS
    KP_PLUS = pygame.K_KP_PLUS
    KP_ENTER = pygame.K_KP_ENTER
    KP_EQUALS = pygame.K_KP_EQUALS


###########################################################
# Font Class
###########################################################

class Font:
    """Font wrapper for Panda2D using pygame."""

    def __init__(self, file: str = None, size: int = 24):
        pygame.font.init()
        self.size = size
        self.file = file
        try:
            if file:
                self.font = pygame.font.Font(file, int(size))
            else:
                self.font = pygame.font.SysFont(None, int(size))
        except Exception:
            self.font = pygame.font.Font(pygame.font.get_default_font(), int(size))

    def set_size(self, size: int):
        self.size = size
        if self.file:
            self.font = pygame.font.Font(self.file, int(size))
        else:
            self.font = pygame.font.SysFont(None, int(size))

    def new_size(self, size: int):
        return Font(self.file, int(size))


###########################################################
# Color Class
###########################################################

class Color:
    """RGBA color representation for Panda2D."""

    def __init__(self, r: int, g: int, b: int, a=255):
        self.r = max(0, min(255, int(r)))
        self.g = max(0, min(255, int(g)))
        self.b = max(0, min(255, int(b)))
        if isinstance(a, float) and 0.0 <= a <= 1.0:
            alpha = int(a * 255)
        else:
            try:
                a_val = float(a)
                if 0 <= a_val <= 1:
                    alpha = int(a_val * 255)
                elif 1 < a_val <= 100:
                    alpha = int(a_val * 255 / 100.0)
                else:
                    alpha = int(a_val)
            except Exception:
                alpha = 255
        self.a = max(0, min(255, alpha))

    def to_tuple(self):
        return (self.r, self.g, self.b, self.a)

    def rgb_tuple(self):
        return (self.r, self.g, self.b)
    
    def mix(self, other: 'Color', factor: float = 0.5) -> 'Color':
        """Mix this color with another color by a given factor (0.0 to 1.0)."""
        factor = max(0.0, min(1.0, factor))
        r = int(self.r * (1 - factor) + other.r * factor)
        g = int(self.g * (1 - factor) + other.g * factor)
        b = int(self.b * (1 - factor) + other.b * factor)
        a = int(self.a * (1 - factor) + other.a * factor)
        return Color(r, g, b, a)


###########################################################
# Image Class
###########################################################
class Image:
    """Image wrapper for Panda2D using pygame surfaces."""
    def __init__(self, path: str):
        try:
            loaded = pygame.image.load(path)
            if loaded.get_alpha() or loaded.get_flags() & pygame.SRCALPHA:
                self.surface = loaded.convert_alpha()
            else:
                self.surface = loaded.convert()
        except Exception:
            self.surface = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.surface.fill((0, 0, 0, 0))

    def get_width(self):
        """Return the width of the image surface."""
        return self.surface.get_width()

    def get_height(self):
        """Return the height of the image surface."""
        return self.surface.get_height()


###########################################################
# Sound Class
###########################################################
class Sound:
    """Sound wrapper for Panda2D using pygame mixer."""
    def __init__(self, path: str):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.sound = pygame.mixer.Sound(path)
        except Exception:
            self.sound = None
    
    def play(self):
        """Play the sound effect."""
        if self.sound:
            try:
                self.sound.play()
            except Exception:
                pass
    
    def stop(self):
        """Stop the sound effect."""
        if self.sound:
            try:
                self.sound.stop()
            except Exception:
                pass


###########################################################
# Resizable & Anchor Enums
###########################################################
class Resizable(Enum):
    NONE = "none"
    WIDTH = "width"
    HEIGHT = "height"
    BOTH = "both"
    ASPECT = "aspect"


class Anchor(Enum):
    CENTER = "center"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOPLEFT = "topleft"
    TOPRIGHT = "topright"
    BOTTOMLEFT = "bottomleft"
    BOTTOMRIGHT = "bottomright"


###########################################################
# PandaWindow Base Class
###########################################################
class PandaWindow:
    """Base window class for Panda2D games and apps."""
    def __init__(
        self,
        width=800,
        height=600,
        title="Panda2D Window",
        resizable=Resizable.NONE,
        anchor=Anchor.CENTER,
    ):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass

        self.width, self.height = width, height
        self._base_width, self._base_height = width, height
        self.title, self.resizable, self.anchor = title, resizable, anchor
        self._flags = pygame.RESIZABLE if resizable != Resizable.NONE else 0

        self.screen = pygame.display.set_mode((width, height), self._flags)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = False
        self.mousex = 0
        self.mousey = 0
        self.deltatime = 0.0
        self._fonts = {}
        self.mousedownprimary = False
        self.mousedownmiddle = False
        self.mousedownsecondary = False

    # ---------------- Coordinate System ----------------
    def _get_anchor_offset(self):
        """Return window center as origin for Panda2D coordinates."""
        return (self.width // 2, self.height // 2)



    def _panda_to_pygame_x(self, x: float) -> int:
        ox, _ = self._get_anchor_offset()
        return int(ox + x)

    # Panda2D (x, y): x+ right, y+ up, origin at anchor
    # Pygame (px, py): x+ right, y+ down, origin at top-left
    def panda2d_to_pygame(self, x: float, y: float) -> tuple[int, int]:
        """Convert Panda2D coordinates to Pygame coordinates."""
        ox, oy = self._get_anchor_offset()
        px = int(ox + x)
        py = int(oy - y)
        return px, py

    def pygame_to_panda2d(self, px: int, py: int) -> tuple[float, float]:
        """Convert Pygame coordinates to Panda2D coordinates."""
        ox, oy = self._get_anchor_offset()
        x = px - ox
        y = oy - py
        return x, y

    def _get_anchor_pos(self, x, y, w, h, anchor):
        """Calculate position based on anchor for drawing."""
        px, py = self.panda2d_to_pygame(x, y)
        # Anchor is now relative to the drawn object's bounding box
        if anchor == Anchor.CENTER:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.TOP:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.BOTTOM:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.LEFT:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.RIGHT:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.TOPLEFT:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.TOPRIGHT:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.BOTTOMLEFT:
            return px - w // 2, py - h // 2
        elif anchor == Anchor.BOTTOMRIGHT:
            return px - w // 2, py - h // 2
        else:
            return px - w // 2, py - h // 2

    # ---------------- Screen Properties ----------------
    @property
    def screen_left(self):
        x, _ = self.pygame_to_panda2d(0, self.height // 2)
        return x

    @property
    def screen_right(self):
        x, _ = self.pygame_to_panda2d(self.width, self.height // 2)
        return x

    @property
    def screen_bottom(self):
        _, y = self.pygame_to_panda2d(self.width // 2, self.height)
        return y

    @property
    def screen_top(self):
        _, y = self.pygame_to_panda2d(self.width // 2, 0)
        return y

    @property
    def screen_center_x(self):
        return (self.screen_left + self.screen_right) / 2

    @property
    def screen_center_y(self):
        return (self.screen_bottom + self.screen_top) / 2

    @property
    def mouse_world(self):
        mx, my = pygame.mouse.get_pos()
        x, y = self.pygame_to_panda2d(mx, my)
        return x, y

    # ---------------- Keyboard Input ----------------
    def keydown(self, key: Key) -> bool:
        pressed = pygame.key.get_pressed()
        return bool(pressed[key.value])

    # ---------------- Window Resize ----------------
    def _handle_resize(self, w, h):
        if self.resizable == Resizable.NONE:
            return
        elif self.resizable == Resizable.WIDTH:
            h = self.height
        elif self.resizable == Resizable.HEIGHT:
            w = self.width
        elif self.resizable == Resizable.ASPECT:
            ratio = self._base_width / self._base_height if self._base_height != 0 else 1
            if w / h > ratio:
                w = int(h * ratio)
            else:
                h = int(w / ratio)
        self.width, self.height = w, h
        self.screen = pygame.display.set_mode((w, h), self._flags)

    # ---------------- Main Loop ----------------
    def start(self):
        self.running = True
        self.initialize()

        while self.running:
            self.deltatime = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self._handle_resize(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mousedownprimary = True
                    elif event.button == 2:
                        self.mousedownmiddle = True
                    elif event.button == 3:
                        self.mousedownsecondary = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mousedownprimary = False
                    elif event.button == 2:
                        self.mousedownmiddle = False
                    elif event.button == 3:
                        self.mousedownsecondary = False

            self.mousex, self.mousey = self.mouse_world

            self.update()
            self.draw()
            pygame.display.flip()

        try:
            pygame.mixer.quit()
        except Exception:
            pass
        pygame.quit()

    # ---------------- User Override Methods ----------------
    def initialize(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    # ---------------- Drawing Methods ----------------
    def clear(self, color=Color(255, 255, 255)):
        """Clear the screen with a color."""
        if color.a == 255:
            self.screen.fill(color.rgb_tuple())
        else:
            temp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            temp.fill(color.to_tuple())
            self.screen.blit(temp, (0, 0))

    def fill_rect(self, x1, y1, x2, y2, color: Color, outline_thickness=0, outline_color: Color = None):
        """Draw a filled rectangle with optional outline."""
        outline_thickness = int(outline_thickness)
        left, right = min(x1, x2), max(x1, x2)
        bottom, top = min(y1, y2), max(y1, y2)
        sx1, sy1 = self.panda2d_to_pygame(left, bottom)
        sx2, sy2 = self.panda2d_to_pygame(right, top)
        w, h = abs(sx2 - sx1), abs(sy2 - sy1)
        px, py = min(sx1, sx2), min(sy1, sy2)
        rect = pygame.Rect(px, py, w, h)
        if color.a == 255:
            pygame.draw.rect(self.screen, color.rgb_tuple(), rect)
        else:
            temp = pygame.Surface((w, h), pygame.SRCALPHA)
            temp.fill(color.to_tuple())
            self.screen.blit(temp, (px, py))
        if outline_thickness > 0 and outline_color:
            col = outline_color.rgb_tuple() if outline_color.a == 255 else outline_color.to_tuple()
            pygame.draw.rect(self.screen, col, rect, outline_thickness)

    def fill_rounded_rect(self, x1, y1, x2, y2, color: Color, outline_thickness=0, outline_color: Color = None,
                      topleft_roundness: float = 0.0, topright_roundness: float = 0.0,
                      bottomleft_roundness: float = 0.0, bottomright_roundness: float = 0.0, steps: int = 10):
        """Draw a filled rounded rectangle with optional outline."""
        
        left, right = min(x1, x2), max(x1, x2)
        bottom, top = min(y1, y2), max(y1, y2)
        w = right - left
        h = top - bottom

        outline_thickness = int(outline_thickness)

        tl = max(1, min(w, topleft_roundness))
        tr = max(1, min(w, topright_roundness))
        bl = max(1, min(w, bottomleft_roundness))
        br = max(1, min(w, bottomright_roundness))

        points = []

        # Top-left
        if tl > 0:
            cx, cy = left + tl, top - tl
            arc_points = []
            for i in range(steps + 1):
                theta = math.pi/2 + (math.pi/2) * (i/steps)
                arc_points.append((cx + tl * math.cos(theta), cy + tl * math.sin(theta)))
            points.extend(reversed(arc_points))
        else:
            points.append((left, top))

        points.append((right - tr, top))

        # Top-right
        if tr > 0:
            cx, cy = right - tr, top - tr
            arc_points = []
            for i in range(steps + 1):
                theta = 0 + (math.pi/2) * (i/steps)
                arc_points.append((cx + tr * math.cos(theta), cy + tr * math.sin(theta)))
            points.extend(reversed(arc_points[1:]))
        else:
            points.append((right, top))

        # Bottom-right (fixed)
        if br > 0:
            cx, cy = right - br, bottom + br
            arc_points = []
            for i in range(steps + 1):
                theta = math.pi/2 + math.pi + (math.pi/2) * (i/steps)
                arc_points.append((cx + br * math.cos(theta), cy + br * math.sin(theta)))
            points.extend(reversed(arc_points))
        else:
            points.append((right, bottom))

        # Bottom-left
        if bl > 0:
            cx, cy = left + bl, bottom + bl
            arc_points = []
            for i in range(steps + 1):
                theta = math.pi + (math.pi/2) * (i/steps)
                arc_points.append((cx + bl * math.cos(theta), cy + bl * math.sin(theta)))
            points.extend(reversed(arc_points))
        else:
            points.append((left, bottom))

        xlist = [p[0] for p in points]
        ylist = [p[1] for p in points]


        # Remove the last item as requested
        xlist = xlist[:-1]
        ylist = ylist[:-1]

        self.fill_polygon(xlist, ylist, color, outline_thickness, outline_color)


    def draw_line(self, x1, y1, x2, y2, color: Color, thickness=1):
        """Draw a line between two points."""
        sx1, sy1 = self.panda2d_to_pygame(x1, y1)
        sx2, sy2 = self.panda2d_to_pygame(x2, y2)
        col = color.rgb_tuple() if color.a == 255 else color.to_tuple()
        pygame.draw.line(self.screen, col, (sx1, sy1), (sx2, sy2), max(1, int(thickness)))

    def draw_text(self, text, font: Font, x, y, anchor=Anchor.CENTER, color: Color = None):
        """Draw text at a given position with anchor and color."""
        col = color.rgb_tuple() if (color and color.a == 255) else (color.to_tuple() if color else (0, 0, 0))
        surf = font.font.render(text, True, col)
        # Convert anchor position from Panda2D to Pygame coordinates
        px, py = self._get_anchor_pos(x, y, surf.get_width(), surf.get_height(), anchor)
        self.screen.blit(surf, (px, py))

    def draw_image(self, image: Image, x, y, anchor=Anchor.CENTER, xscale=1.0, yscale=1.0,
                   outline_thickness=0, outline_color: Color = None, filter: Color = Color(255, 255, 255, 255), rotation: int = 0):
        """Draw an image at a given position with scaling, color filter, and optional outline."""
        outline_thickness = int(outline_thickness)
        w = max(1, int(image.surface.get_width() * xscale))
        h = max(1, int(image.surface.get_height() * yscale))
        img = pygame.transform.scale(image.surface, (w, h))
        # Apply color filter with transparency
        if filter is not None and (filter.r != 255 or filter.g != 255 or filter.b != 255 or filter.a != 255):
            filter_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            filter_surf.fill(filter.to_tuple())
            img = img.copy()
            img.blit(filter_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            if filter.a < 255:
                alpha_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                alpha_surf.fill((255, 255, 255, filter.a))
                img.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # Apply rotation if needed
        if rotation != 0:
            img = pygame.transform.rotate(img, -rotation)  # Pygame rotates counterclockwise, so negate for clockwise
            w, h = img.get_width(), img.get_height()
        # Convert anchor position from Panda2D to Pygame coordinates
        px, py = self._get_anchor_pos(x, y, w, h, anchor)
        self.screen.blit(img, (px, py))
        if outline_thickness > 0 and outline_color:
            col = outline_color.rgb_tuple() if outline_color.a == 255 else outline_color.to_tuple()
            pygame.draw.rect(self.screen, col, pygame.Rect(px, py, w, h), outline_thickness)

    def fill_polygon(self, xlist, ylist, color: Color, outline_thickness=0, outline_color: Color = None):
        """Draw a filled polygon with optional outline."""
        if not xlist or not ylist or len(xlist) != len(ylist):
            return
        points = [self.panda2d_to_pygame(x, y) for x, y in zip(xlist, ylist)]
        if color.a == 255:
            pygame.draw.polygon(self.screen, color.rgb_tuple(), points, 0)
        else:
            # Create a temporary surface for alpha blending
            min_x = min(p[0] for p in points)
            min_y = min(p[1] for p in points)
            max_x = max(p[0] for p in points)
            max_y = max(p[1] for p in points)
            w = max_x - min_x + 1
            h = max_y - min_y + 1
            temp = pygame.Surface((w, h), pygame.SRCALPHA)
            shifted_points = [(p[0] - min_x, p[1] - min_y) for p in points]
            temp.fill((0, 0, 0, 0))
            pygame.draw.polygon(temp, color.to_tuple(), shifted_points, 0)
            self.screen.blit(temp, (min_x, min_y))
        if outline_thickness > 0 and outline_color:
            col = outline_color.rgb_tuple() if outline_color.a == 255 else outline_color.to_tuple()
            pygame.draw.polygon(self.screen, col, points, outline_thickness)
