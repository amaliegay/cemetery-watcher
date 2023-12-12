from os import listdir
from os.path import isfile, join

import pygame
from settings import *
from utils import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.import_assets()
        self.status = "down_idle"
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=position)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        print("import_assets")
        self.animations = {
            # "up": [],
            # "down": [],
            # "left": [],
            # "right": [],
            # "up_idle": [],
            "down_idle": [],
            # "left_idle": [],
            # "right_idle": [],
            # "up_sledgehammer": [],
            # "down_sledgehammer": [],
            # "left_sledgehammer": [],
            # "right_sledgehammer": [],
            # "up_knife": [],
            # "down_knife": [],
            # "left_knife": [],
            # "right_knife": [],
            # "up_revolver": [],
            # "down_revolver": [],
            # "left_revolver": [],
            # "right_revolver": [],
        }

        for animation in self.animations.keys():
            full_path = "assets/npc/" + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, deltaTime):
        self.frame_index += 4 * deltaTime
        self.image = self.animations[self.status][self.frame_index]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            print("keyDown (scanCode = keyUp)")
            self.direction.y = -1
        elif keys[pygame.K_w]:
            print("keyDown (scanCode = w)")
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            print("keyDown (scanCode = keyDown)")
            self.direction.y = 1
        elif keys[pygame.K_s]:
            print("keyDown (scanCode = s)")
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            print("keyDown (scanCode = keyLeft)")
            self.direction.x = -1
        elif keys[pygame.K_a]:
            print("keyDown (scanCode = a)")
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            print("keyDown (scanCode = keyRight)")
            self.direction.x = 1
        elif keys[pygame.K_d]:
            print("keyDown (scanCode = d)")
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, deltaTime):
        # normalize the direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.position.x += self.speed * self.direction.x * deltaTime
        self.rect.centerx = self.position.x

        # vertical movement
        self.position.y += self.speed * self.direction.y * deltaTime
        self.rect.centery = self.position.y

    def update(self, deltaTime):
        self.input()
        self.move(deltaTime)


def load_sprite_sheets(dir1, dir2, width, height):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))


class Actor(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, id):
        self.sprites = load_sprite_sheets("Actors", id, width, height)

    def draw(self, win):
        self.sprite = self.sprites["idle"][0]
        win.blit(self.sprite, (self.bounding_box.x, self.bounding_box.y))
