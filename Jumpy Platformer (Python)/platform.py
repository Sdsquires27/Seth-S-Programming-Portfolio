import pygame as pg
from settings import *
from random import choice

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        super(Platform, self).__init__()
        images = [game.platformImageBig, game.platformImageSmall]
        resized = []
        for image in images:
            imageRect = image.get_rect()
            image = pg.transform.scale(image, (imageRect.width // 2, imageRect.height // 2))
            resized.append(image)
        self.image = choice(resized)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
