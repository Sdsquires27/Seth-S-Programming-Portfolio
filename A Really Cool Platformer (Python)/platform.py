from settings import *
import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, game, w, h):
        self._layer = PLATFORM_LAYER
        self.groups = game.allSprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

