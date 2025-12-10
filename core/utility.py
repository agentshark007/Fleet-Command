import math

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def mouse_in_area(mousex: float, mousey: float, x1: float, x2: float, y1: float, y2: float) -> bool:
    # Sort coordinates to ensure proper bounds
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    
    return x1 <= mousex <= x2 and y1 <= mousey <= y2

def pseudo_random_offset(x: float, y: float, seed: int = 0) -> float:
    return (math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453) % 1
