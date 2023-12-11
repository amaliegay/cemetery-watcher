from os.path import join

import pygame

from settings import *
from player import Player


class Level:
    def __init__(self):
        print("Level init")

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

        # get the map
        # map, image = get_map("daisy_dirt_01.png")

        # draw(window, map, image, zombie)
        # pygame.transform.scale_by(window, SCALE)

    def simulate(self, deltaTime):
        print("Level.simulate (deltaTime = " + str(deltaTime) + ")")
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(deltaTime)


def draw(window, map, image, actor):
    # draw the map
    for tile in map:
        window.blit(image, tile)


def get_map(name):
    json_path = join("assets", "Maps", name)
    image = pygame.image.load(join("assets", "Maps", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

    # open json file
    # map_file = open(json_path)

    # returns json object as a dictionary
    # map_data = json.load(map_file)
    # images = []

    # iterating through the json list
    # for tilesheet in map_data["tilesheets"]:
    #     image = pygame.image.load(join("assets", "Maps", tilesheet["file_path"]))
    #     images.append(image)

    # Closing file
    # map_file.close()

    # tiles = []
    # for layer in map_data["map"]:
    #     for i in layer:
    #         tiles.append([])
    #         for j in layer[i]:
    #             tiles[int(i)].append(layer[i][j])

    # return tiles, images
