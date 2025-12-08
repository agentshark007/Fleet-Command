from enum import Enum

class ExtendMethod(Enum):
    """Direction for extension operations."""
    LEFT = -1   # Used for horizontal extension
    RIGHT = 1   # Used for horizontal extension
    UP = 1      # Used for vertical extension
    DOWN = -1   # Used for vertical extension




class Extension:
    """Handles scaling and extension logic for UI elements."""

    def __init__(self):
        self.scale = 1.0

    def extend(self, pivot, value, direction: ExtendMethod):
        """Extend a value from a pivot in a given direction, scaled."""
        return pivot + (value * direction.value * self.scale)
