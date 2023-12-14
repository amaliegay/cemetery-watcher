from os import listdir
from os.path import isfile, join

import pygame
from settings import *
from utils import *
from animations import *
from timer import Timer


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

        # timers
        self.timers = {"tool use": Timer(duration=350, callback=self.use_tool)}

        # equipments
        self.equipped_tool = "hoe"

    def use_tool(self):
        print("use_tool")

    def import_assets(self):
        print("import_assets")
        self.animations = animations

        for animation in animations.keys():
            surface_list = []
            for frame in animations[animation]:
                full_path = "assets/Characters/" + frame["image"]

                sprite_sheet = pygame.image.load(full_path).convert_alpha()
                surface = pygame.Surface(
                    (frame["size"]["width"], frame["size"]["height"]),
                    pygame.SRCALPHA,
                    32,
                )
                selected = pygame.Rect(
                    frame["starting_position"]["x"],
                    frame["starting_position"]["y"],
                    frame["size"]["width"],
                    frame["size"]["height"],
                )
                surface.blit(sprite_sheet, (0, 0), selected)
                surface_list.append(pygame.transform.scale_by(surface, SCALE))

            self.animations[animation] = surface_list

    def animate(self, deltaTime):
        self.frame_index += 4 * deltaTime
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["tool use"].active:
            # directions
            if keys[pygame.K_UP]:
                print("keyDown (scanCode = keyUp)")
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_w]:
                print("keyDown (scanCode = w)")
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                print("keyDown (scanCode = keyDown)")
                self.direction.y = 1
                self.status = "down"
            elif keys[pygame.K_s]:
                print("keyDown (scanCode = s)")
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                print("keyDown (scanCode = keyLeft)")
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_a]:
                print("keyDown (scanCode = a)")
                self.direction.x = -1
                self.status = "left"
            elif keys[pygame.K_RIGHT]:
                print("keyDown (scanCode = keyRight)")
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_d]:
                print("keyDown (scanCode = d)")
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            # equip
            if keys[pygame.K_TAB]:
                self.timers["tool use"].start()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # tool use
        if self.timers["tool use"].active:
            self.status = self.status.split("_")[0] + "_" + self.equipped_tool

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

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, deltaTime):
        self.input()
        self.get_status()
        self.update_timer()
        self.move(deltaTime)
        self.animate(deltaTime)
