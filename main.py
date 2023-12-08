import os
from os import listdir
from os.path import isfile, join
import random
import math
import numpy as np 

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
pygame.display.set_caption("SHOOTER")

FPS = 60

class Actor(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height):
        self.bounding_box = pygame.Rect(x, y, width, height)
        self.velocity = np.array([0,0]) 


def draw(window, background):
    # draw the background image
    window.bilt(background, (0,0))
    pygame.display.update()


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    return image


def main(window):
    clock = pygame.time.Clock()

    # get the background image
    background = get_background("cemetery.png")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(background)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
