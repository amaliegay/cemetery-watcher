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
        self.z = LAYERS["main"]

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            "tool_use": Timer(duration=200, callback=self.use_tool),
            "tool_switch": Timer(duration=200)
            "spell_switch": Timer(duration=200)
        }

        # inventory
        self.inventory = ["axe", "hoe", "water"]
        self.readied_tool_index = 0
        self.readied_tool = self.inventory[self.readied_tool_index]

        # spells
        self.spells = ["corn", "tomato"]
        self.readied_spell_index = 0
        self.readied_spell = self.spells[self.readied_spell_index]
        

    def use_tool(self):
        print("use_tool")

    def change_tool(self):
        self.timers["tool_switch"].start()
        self.readied_tool_index += 1
        self.readied_tool_index = self.readied_tool_index if self.readied_tool_index < len(self.inventory) else 0
        self.readied_tool = self.inventory[self.readied_tool_index]

    def change_spell(self):
        self.timers["spell_switch"].start()
        self.readied_spell_index += 1
        self.readied_spell_index = self.readied_spell_index if self.readied_spell_index < len(self.spells) else 0
        self.readied_spell = self.spells[self.readied_spell_index]

    def import_assets(self):
        print("import_assets")
        self.animations = animations

        for animation in animations.keys():
            surface_list = []
            for frame in animations[animation]:
                surface_list.append(import_asset("assets/Characters/", frame))

            self.animations[animation] = surface_list

    def animate(self, deltaTime):
        self.frame_index += 4 * deltaTime
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["tool_use"].active:
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

            # use tool
            mouse_click, _, _ = pygame.mouse.get_pressed()
            if mouse_click:
                self.timers["tool_use"].start()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

    def get_status(self):
        # idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # tool use
        if self.timers["tool_use"].active:
            self.status = self.status.split("_")[0] + "_" + self.readied_tool

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
