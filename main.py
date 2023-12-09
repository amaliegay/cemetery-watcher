import os
from os import listdir
from os.path import isfile, join
import random
import math
import numpy as np
import json

# import pygame module
import pygame

pygame.init()

# screen size [width, height]
WIDTH, HEIGHT = 600, 600
SCREEN_SIZE = [WIDTH, HEIGHT]

# setting the size of the window
window = pygame.display.set_mode(SCREEN_SIZE)

# store the color
WHITE = (255, 255, 255)
BG_COLOR = WHITE

# set caption of screen
pygame.display.set_caption("Cemetery Watcher")

FPS = 60


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
        self.velocity = np.array([0, 0])
        self.mask = None
        self.orientation = np.array([0, 1])
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


def draw(window, map, images, actor):
    # draw the map
    window.blit(images[0], (0, 0))
    # actor.draw(window)
    pygame.display.update()


def get_map(name):
    json_path = join("assets", "Maps", name)
    # open json file
    map_file = open(json_path)

    # returns json object as a dictionary
    map_data = json.load(map_file)
    images = []

    # iterating through the json list
    for tilesheet in map_data["tilesheets"]:
        image = pygame.image.load(join("assets", "Maps", tilesheet["file_path"]))
        images.append(image)

    # Closing file
    map_file.close()

    tiles = []
    for layer in map_data["map"]:
        for i in layer:
            tiles.append([])
            for j in layer[i]:
                tiles[int(i)].append(layer[i][j])

    return tiles, images


def handle_move(actor):
    actor.velocity = np.array([0, 0])
    actor.move_forward()


def main(window):
    clock = pygame.time.Clock()

    # get the map
    map, images = get_map("cemetery.json")

    zombie = Actor(x=275, y=50, width=32, height=32, id="Zombie")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        zombie.simulate(FPS)
        handle_move(zombie)
        draw(window, map, images, zombie)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
