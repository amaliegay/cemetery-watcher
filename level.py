from os.path import join

import pygame

from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Wildflower, Tree, Zombie
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):
        print("Level init")

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.zombie_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame("Data Files/map.tmx")

        generic_layers = {"main": ["Tombstones", "Fences"]}
        for layers_id in generic_layers.keys():
            for layer in generic_layers[layers_id]:
                for x, y, surface in tmx_data.get_layer_by_name(layer).tiles():
                    Generic(
                        position=(x * TILE_SIZE, y * TILE_SIZE),
                        surface=surface,
                        groups=[self.all_sprites, self.collision_sprites],
                        z=LAYERS[layers_id],
                    )

        for x, y, surface in tmx_data.get_layer_by_name("Decoration").tiles():
            Wildflower(
                position=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=[self.all_sprites, self.collision_sprites],
            )

        for x, y, surface in tmx_data.get_layer_by_name("Trees").tiles():
            Tree(
                position=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=[self.all_sprites, self.collision_sprites],
            )

        for x, y, surface in tmx_data.get_layer_by_name("Zombies").tiles():
            Zombie(
                position=(x * TILE_SIZE, y * TILE_SIZE),
                surface=surface,
                groups=[self.all_sprites, self.collision_sprites, self.zombie_sprites],
            )

        # collision tiles
        for x, y, surface in tmx_data.get_layer_by_name("Collision").tiles():
            Generic(
                (x * TILE_SIZE, y * TILE_SIZE),
                pygame.Surface((TILE_SIZE, TILE_SIZE)),
                self.collision_sprites,
            )

        # player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Spawn":
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites,
                    self.zombie_sprites,
                )

    def simulate(self, deltaTime):
        # print("Level.simulate (deltaTime = " + str(deltaTime) + ")")
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(deltaTime)

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x, self.offset.y = (
            player.rect.centerx - WIDTH / 2,
            player.rect.centery - HEIGHT / 2,
        )
        for layer in LAYERS.values():
            for sprite in sorted(
                self.sprites(), key=lambda sprite: sprite.rect.centery
            ):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
