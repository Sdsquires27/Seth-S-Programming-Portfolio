import pygame as pg
from settings import *

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(Platform, self).__init__()
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
