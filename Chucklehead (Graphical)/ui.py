from settings import *
import pygame as pg


class PgButton(pg.sprite.Sprite):
    def __init__(self, sprite, discard):
        super(PgButton, self).__init__()
        self.image = pg.transform.scale(sprite, (300, 100))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (WIDTH - 200, HEIGHT / 4)
        self.curPlayer = None
        self.discard = discard

    def setPlayer(self, player):
        self.curPlayer = player

    def click(self):
        x, y = pg.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if self.discard.discard.cards:
                self.discard.giveToHand(self.curPlayer.hand)

