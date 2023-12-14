import pygame


class Timer:
    def __init__(self, duration, callback=None):
        self.duration = duration
        self.callback = callback
        self.start_time = 0
        self.active = False

    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        
    def cancel(self):
        self.active = False
        self.start_time = 0
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.cancel()
            if self.callback:
                self.callback()