from os import listdir
from os.path import isfile, join

import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        # general setup
        self.image = pygame.Surface((32, 64))
        self.image.fill("green")
        self.rect = self.image.get_rect(center=position)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

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
        self.position += self.speed * self.direction * deltaTime
        self.rect.center = self.position

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
