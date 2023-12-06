import os
from os import listdir
from os.path import isfile, join
import random
import math

import pygame

pygame.init()

pygame.display.set_caption("SHOOTER")

WHITE = (255, 255, 255)
BG_COLOR = WHITE
WIDTH, HEIGHT = 600, 600
FPS = 60
PLAYER_VELOCITY = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    return image


def main(window):
    clock = pygame.time.Clock()
    background = get_background("cemetery.png")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
