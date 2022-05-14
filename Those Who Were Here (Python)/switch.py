from settings import *
import pygame as pg


class Switch(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = SWITCH_LAYER
        self.groups = game.allSprites, game.switches
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.upImage = pg.transform.scale(self.game.pushButtonUp, (TILESIZE, 50))
        self.upImage.set_colorkey(BLACK)
        self.downImage = pg.transform.scale(self.game.pushButtonDown, (TILESIZE, 32))
        self.downImage.set_colorkey(BLACK)
        self.image = self.upImage
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.y += TILESIZE
        self.x += self.rect.width / 2
        self.rect.midbottom = self.x, self.y
        self.selected = False

    def update(self):
        self.image = self.upImage
        hits = pg.sprite.spritecollide(self, self.game.objects, False)
        self.selected = False
        if hits:
            self.image = self.downImage
            self.selected = True
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.x, self.y
