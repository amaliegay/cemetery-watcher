from os import listdir
from os.path import isfile, join

import pygame

from settings import *


class Level:
    def __init__(self):
        print("Level init")

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        # zombie.simulate(FPS)

        # get the map
        # map, image = get_map("daisy_dirt_01.png")

        # zombie = Actor(x=275, y=50, width=32, height=32, id="Zombie")

        # handle_move(zombie)
        # draw(window, map, image, zombie)
        # pygame.transform.scale_by(window, SCALE)

    def simulate(self, deltaTime):
        print("Level.simulate (deltaTime = " + str(deltaTime) + ")")
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()


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
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height, id):
        self.sprites = load_sprite_sheets("Actors", id, width, height)
        self.bounding_box = pygame.Rect(x, y, width, height)
        self.velocity = Vector2(0, 0)
        self.mask = None
        self.orientation = Vector2(0, 1)
        self.move_speed = 5

    def move(self, velocity):
        self.bounding_box.x += velocity[0]
        self.bounding_box.y += velocity[1]

    def move_forward(self):
        self.velocity[1] = self.move_speed

    def simulate(self, fps):
        self.move(self.velocity)

    def draw(self, win):
        self.sprite = self.sprites["idle"][0]
        win.blit(self.sprite, (self.bounding_box.x, self.bounding_box.y))


def draw(window, map, image, actor):
    # draw the map
    for tile in map:
        window.blit(image, tile)

    # actor.draw(window)


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


def handle_move(actor):
    actor.velocity = Vector2(0, 0)
    actor.move_forward()
