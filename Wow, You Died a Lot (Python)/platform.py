from settings import *
import pygame as pg
from enemy import *

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, type, game):
        self._layer = PLATFORM_LAYER
        if type == "P":
            self.groups = game.allSprites, game.platforms
        elif type == "O":
            self.groups = game.allSprites, game.obstacles
            self._layer -= 1
        elif type == "PO":
            self.groups = game.allSprites, game.obstacles
            self._layer -= 1
        elif type == "G":
            self.groups = game.allSprites, game.goal
        else:
            self.groups = game.allSprites

        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        if type == "P":
            self.image.fill(GREEN)
        if type == "PO":
            self.image.fill(RED)
        elif type == "O":
            self.image = pg.transform.scale(game.enemySpritesheet.getImage(136, 66, 51, 51), (w, w))
            self.image.set_colorkey(BLACK)
        elif type == "G":
            self.image = pg.transform.scale(game.doorImage, (w, h))
            self.image.set_colorkey(WHITE)

        # this is essentially a workaround so that level generation doesn't have to be changed.
        # this means if the type is mob, it will delete itself and make a mob instead.
        elif type == "M":
            Enemy(game, x, y, w , h)
            self.kill()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

