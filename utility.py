import math

def distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def mouse_in_area(mousex, mousey, x1, x2, y1, y2):
    """Check if the mouse coordinates are within a specified rectangular area."""
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    
    return x1 <= mousex <= x2 and y1 <= mousey <= y2
