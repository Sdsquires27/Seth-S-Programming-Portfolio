from settings import *
import pygame as pg


class PgButton(pg.sprite.Sprite):
    def __init__(self, sprite, darkSprite, discard):
        super(PgButton, self).__init__()
        self.normalImage = pg.transform.scale(sprite, (300, 100))
        self.darkImage = pg.transform.scale(darkSprite, (300, 100))
        self.image = self.normalImage
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.center = (WIDTH - 200, HEIGHT / 4)
        self.curPlayer = None
        self.discard = discard

    def setPlayer(self, player):
        self.curPlayer = player

    def update(self):
        # if being touched by mouse, change image
        self.image = self.normalImage
        x, y = pg.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.image = self.darkImage

    def click(self):
        x, y = pg.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            # give discard to current player
            if self.discard.discard.cards:
                self.discard.giveToHand(self.curPlayer.hand)

