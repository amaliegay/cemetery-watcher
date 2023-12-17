import pygame
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, z=LAYERS["main"]):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.z = z
        self.bounding_box = self.rect.copy().inflate(
            -self.rect.width * 0.4, -self.rect.height * 0.75
        )
        print(
            f"Generic: rect = ({self.rect.width}, {self.rect.height}), bounding_box = ({self.bounding_box.width}, {self.bounding_box.height})"
        )


class Wildflower(Generic):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        self.bounding_box = self.rect.copy().inflate(-8, -self.rect.height * 0.9)
        print(
            f"Wildflower: rect = ({self.rect.width}, {self.rect.height}), bounding_box = ({self.bounding_box.width}, {self.bounding_box.height})"
        )


class Tree(Generic):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        self.bounding_box = self.rect.copy().inflate(
            -self.rect.width * 0.9, -self.rect.height * 0.5
        )
        print(
            f"Tree: rect = ({self.rect.width}, {self.rect.height}), bounding_box = ({self.bounding_box.width}, {self.bounding_box.height})"
        )
