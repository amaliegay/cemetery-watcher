from pygame.math import Vector2

# screen size [width, height]
TILE_SIZE = 16
WIDTH, HEIGHT = 240, 192
SCREEN_SIZE = [WIDTH, HEIGHT]
FPS = 60

# overlay
OVERLAY_POSITION = {"tool": (16, HEIGHT - 8), "spell": (32, HEIGHT - 8)}

PLAYER_TOOL_OFFSET = {
    "left": Vector2(-9, 6),
    "right": Vector2(8, 7),
    "up": Vector2(3, -11),
    "down": Vector2(-4, 10),
}


# store the color
WHITE = (255, 255, 255)

# layers
LAYERS = {"ground": 0, "soil": 1, "ground plant": 2, "main": 3, "zombies": 4}
