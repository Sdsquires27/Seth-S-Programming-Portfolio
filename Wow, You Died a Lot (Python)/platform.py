from settings import *
import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, type, game):
        self._layer = PLATFORM_LAYER
        if type == "P":
            self.groups = game.allSprites, game.platforms
        elif type == "O":
            self.groups = game.allSprites, game.obstacles
        elif type == "G":
            self.groups = game.allSprites, game.goal

        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        if type == "P":
            self.image.fill(GREEN)
        elif type == "O":
            self.image.fill(RED)
        elif type == "G":
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

