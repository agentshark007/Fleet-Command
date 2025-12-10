class Camera:
    """Simple 2D camera for transforming between world and screen coordinates.
    
    Provides projection and deduction methods to transform coordinates between
    world space and screen space, with support for camera position and zoom level.
    """

    def __init__(self, x: float, y: float, scale: float):
        """Initialize the camera.
        
        Args:
            x: Camera position in world space (horizontal).
            y: Camera position in world space (vertical).
            scale: Camera zoom level (1.0 = normal, > 1.0 = zoomed in, < 1.0 = zoomed out).
        """
        self.x: float = x  # Camera world position (X)
        self.y: float = y  # Camera world position (Y)
        self.scale: float = scale  # Zoom level
        self.velocity_x: float = 0.0  # Horizontal velocity for smooth camera movement
        self.velocity_y: float = 0.0  # Vertical velocity for smooth camera movement

    def project(self, x: float, y: float) -> tuple[float, float]:
        """Project world-space coordinates to screen-space.
        
        Transforms coordinates from the game world into screen coordinates,
        accounting for camera position and zoom level.
        
        Args:
            x: World space X coordinate.
            y: World space Y coordinate.
            
        Returns:
            Tuple of (screen_x, screen_y) coordinates.
        """
        x = (x - self.x) * self.scale  # Translate and scale for horizontal
        y = (y - self.y) * self.scale  # Translate and scale for vertical
        return x, y

    def deduce(self, x: float, y: float) -> tuple[float, float]:
        """Convert screen-space coordinates to world-space.
        
        Performs the inverse transformation of project(), converting screen
        coordinates back to world coordinates using camera position and zoom.
        
        Args:
            x: Screen space X coordinate.
            y: Screen space Y coordinate.
            
        Returns:
            Tuple of (world_x, world_y) coordinates.
        """
        x = x / self.scale + self.x  # Unscale and translate horizontal
        y = y / self.scale + self.y  # Unscale and translate vertical
        return x, y
