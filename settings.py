from pygame.math import Vector2

# screen size [width, height]
TILE_SIZE = 16
WIDTH, HEIGHT = 1280, 720
SCREEN_SIZE = [WIDTH, HEIGHT]
SCALE = 4

# overlay
OVERLAY_POSITION = {
    "tool": (40, HEIGHT - 15)
    "spell": (70, HEIGHT - 5)
}

FPS = 60

# store the color
WHITE = (255, 255, 255)

# layers
LAYERS = {"ground": 0, "soil": 1, "ground plant": 2, "main": 3}
