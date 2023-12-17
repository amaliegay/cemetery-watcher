import pygame

from settings import *
from utils import *


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


class Particle(Generic):
    def __init__(self, position, surface, groups, z, duration=100):
        super().__init__(position, surface, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surface = pygame.mask.from_surface(self.image)
        new_surface = mask_surface.to_surface()
        new_surface.set_colorkey((0, 0, 0))
        self.image = new_surface

    def update(self, deltaTime):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        self.bounding_box = self.rect.copy().inflate(
            -self.rect.width * 0.9, -self.rect.height * 0.5
        )
        print(
            f"Tree: rect = ({self.rect.width}, {self.rect.height}), bounding_box = ({self.bounding_box.width}, {self.bounding_box.height})"
        )


class Zombie(Generic):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        self.bounding_box = self.rect.copy().inflate(
            -self.rect.width * 0.9, -self.rect.height * 0.5
        )
        print(
            f"Zombie: rect = ({self.rect.width}, {self.rect.height}), bounding_box = ({self.bounding_box.width}, {self.bounding_box.height})"
        )

        # zombie attributes
        self.health = 5
        self.isDead = False

    def damage(self):
        # damage the zombie
        print("damage zombie")
        self.health -= 1
        Particle((self.rect.topleft), self.image, self.groups()[0], LAYERS["main"])

    def check_death(self):
        if self.health <= 0:
            self.image = import_asset(
                "assets/Characters/",
                {
                    "image": "Egg_And_Nest.png",
                    "starting_position": {"x": 0, "y": 0},
                    "size": {"width": 16, "height": 16},
                },
            )
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.bounding_box = self.rect.copy().inflate(-10, -self.rect.height * 0.8)
            self.isDead = True
            print("zombie is dead")

    def update(self, deltaTime):
        if not self.isDead:
            self.check_death()
