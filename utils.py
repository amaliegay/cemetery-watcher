import pygame

def import_asset(path, object):
    full_path = path + object["image"]

    sprite_sheet = pygame.image.load(full_path).convert_alpha()
    surface = pygame.Surface(
        (object["size"]["width"], object["size"]["height"]),
        pygame.SRCALPHA,
        32,
    )
    selected = pygame.Rect(
        object["starting_position"]["x"],
        object["starting_position"]["y"],
        object["size"]["width"],
        object["size"]["height"],
    )
    surface.blit(sprite_sheet, (0, 0), selected)
    return pygame.transform.scale_by(surface, SCALE)