import math
from typing import Union
from libraries.pgiud import V

def distance(x1: Union[float, V], y1: Union[float, V], x2: float=None, y2: float=None) -> float:
    if isinstance(x1, V) and isinstance(y1, V):
        return math.sqrt((y1.x - x1.x) ** 2 + (y1.y - x1.y) ** 2)
    if x2 is None or y2 is None:
        raise ValueError('distance requires either two V instances or four numeric args')
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def mouse_in_area(mousex: Union[float, V], mousey: float, x1: float, x2: float, y1: float, y2: float) -> bool:
    if isinstance(mousex, V):
        mx, my = (mousex.x, mousex.y)
    else:
        mx, my = (mousex, mousey)
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    return x1 <= mx <= x2 and y1 <= my <= y2

def pseudo_random_offset(x: float, y: float, seed: int=0) -> float:
    return math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453 % 1
