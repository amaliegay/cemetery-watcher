from os import listdir
from os.path import isfile, join

import pygame
from settings import *
from utils import *
from animations import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, position, group, collision_sprites, zombie_sprites, interaction):
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
        self.speed = 100

        # collision
        self.collision_sprites = collision_sprites
        self.bounding_box = self.rect.copy().inflate((-36, -32))
        print(
            f"Player: rect = ({self.rect.width}, {self.rect.height}), bounding_box = ({self.bounding_box.width}, {self.bounding_box.height})"
        )

        # timers
        self.timers = {
            "tool_use": Timer(duration=350, callback=self.use_tool),
            "tool_switch": Timer(duration=200),
            "spell_switch": Timer(duration=200),
        }

        # inventory
        self.inventory = ["axe", "hoe", "water"]
        self.readied_tool_index = 0
        self.readied_tool = self.inventory[self.readied_tool_index]

        # spells
        self.spells = ["corn", "tomato"]
        self.readied_spell_index = 0
        self.readied_spell = self.spells[self.readied_spell_index]

        # interaction
        self.zombie_sprites = zombie_sprites
        self.interaction = interaction

    def get_target_position(self):
        self.target_position = (
            self.rect.center + PLAYER_TOOL_OFFSET[self.status.split("_")[0]]
        )

    def use_tool(self):
        if self.readied_tool == "axe":
            for zombie in self.zombie_sprites.sprites():
                if zombie.rect.collidepoint(self.target_position):
                    zombie.damage()
        if self.readied_tool == "hoe":
            pass
        if self.readied_tool == "water":
            pass

    def change_tool(self, direction):
        self.timers["tool_switch"].start()
        if direction == "up":
            self.readied_tool_index -= 1
        elif direction == "down":
            self.readied_tool_index += 1
        self.readied_tool_index = self.readied_tool_index % len(self.inventory)
        self.readied_tool = self.inventory[self.readied_tool_index]

    def change_spell(self, direction):
        self.timers["spell_switch"].start()
        if direction == "up":
            self.readied_spell_index -= 1
        elif direction == "down":
            self.readied_spell_index += 1
        self.readied_spell_index = self.readied_spell_index % len(self.spells)
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

            if keys[pygame.K_SPACE]:
                print("keyDown (scanCode = space)")
                collided_interaction_sprite = pygame.sprite.spritecollide(
                    self, self.interaction, False
                )
                print(collided_interaction_sprite)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == "Gate":
                        print("activate Gate")

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

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "bounding_box"):
                if sprite.bounding_box.colliderect(self.bounding_box):
                    if direction == "horizontal":
                        if self.direction.x > 0:
                            self.bounding_box.right = sprite.bounding_box.left
                        if self.direction.x < 0:
                            self.bounding_box.left = sprite.bounding_box.right
                        self.rect.centerx = self.bounding_box.centerx
                        self.position.x = self.bounding_box.centerx

                    if direction == "vertical":
                        if self.direction.y > 0:
                            self.bounding_box.bottom = sprite.bounding_box.top
                        if self.direction.y < 0:
                            self.bounding_box.top = sprite.bounding_box.bottom
                        self.rect.centery = self.bounding_box.centery
                        self.position.y = self.bounding_box.centery

    def move(self, deltaTime):
        # normalize the direction vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.position.x += self.speed * self.direction.x * deltaTime
        self.bounding_box.centerx = round(self.position.x)
        self.rect.centerx = self.bounding_box.centerx
        self.collision("horizontal")

        # vertical movement
        self.position.y += self.speed * self.direction.y * deltaTime
        self.bounding_box.centery = round(self.position.y)
        self.rect.centery = self.bounding_box.centery
        self.collision("vertical")

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, deltaTime):
        self.input()
        self.get_status()
        self.update_timer()
        self.get_target_position()
        self.move(deltaTime)
        self.animate(deltaTime)
