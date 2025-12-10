"""Utility functions for common game calculations.

This module contains helper functions for distance calculations, collision detection,
and coordinate checks used throughout the game.
"""

import math

def distance(x1, y1, x2, y2):
    """Calculate the Euclidean distance between two points.
    
    Args:
        x1: X coordinate of first point.
        y1: Y coordinate of first point.
        x2: X coordinate of second point.
        y2: Y coordinate of second point.
        
    Returns:
        The straight-line distance between the two points.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def mouse_in_area(mousex, mousey, x1, x2, y1, y2):
    """Check if mouse coordinates are within a rectangular area.
    
    Performs an axis-aligned bounding box (AABB) check. Automatically handles
    x1/x2 and y1/y2 being in any order.
    
    Args:
        mousex: Mouse X coordinate.
        mousey: Mouse Y coordinate.
        x1: First X boundary.
        x2: Second X boundary.
        y1: First Y boundary.
        y2: Second Y boundary.
        
    Returns:
        True if the mouse is within the rectangular area, False otherwise.
    """
    # Sort coordinates to ensure proper bounds
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    
    return x1 <= mousex <= x2 and y1 <= mousey <= y2

def pseudo_random_offset(x, y, seed=0):
    """Generate a pseudo-random offset based on coordinates and a seed."""
    return (math.sin(x * 12.9898 + y * 78.233 + seed) * 43758.5453) % 1
