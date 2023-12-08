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
pygame.display.set_caption("Cemetery Watcher")

FPS = 60


class Actor(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height):
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
        pygame.draw.rect(win, self.COLOR, self.bounding_box)


def draw(window, background, actor):
    # draw the background image
    window.blit(background, (0, 0))
    actor.draw(window)
    pygame.display.update()


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    return image


def handle_move(actor):
    actor.velocity = np.array([0, 0])
    actor.move_forward()


def main(window):
    clock = pygame.time.Clock()

    # get the background image
    background = get_background("cemetery.png")

    zombie = Actor(x=275, y=50, width=50, height=50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        zombie.simulate(FPS)
        handle_move(zombie)
        draw(window, background, zombie)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
