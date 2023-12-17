import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.z = z


class Wildflower(Generic):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)


class Tree(Generic):
    def __init__(self, position, surface, groups, name):
        super().__init__(position, surface, groups)
