import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super(Player, self).__init__()
        self.image = pygame.Surface((30, 30))
        self.image = sprite
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.rect.x += 5
        self.rect.y += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0