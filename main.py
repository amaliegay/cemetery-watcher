import sys

# import pygame module
import pygame

from settings import *
from level import Level
from event_handler import *


class Game:
    def __init__(self):
        pygame.init()

        # setting the size of the window
        flags = pygame.SCALED
        self.screen = pygame.display.set_mode(SCREEN_SIZE, flags)

        # set caption of screen
        pygame.display.set_caption("The Cemetery Watcher")

        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                event_handler(event, self.level)

            deltaTime = self.clock.tick(FPS) / 1000
            self.level.simulate(deltaTime)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
