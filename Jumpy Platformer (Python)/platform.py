import pygame as pg
from settings import *
from random import choice
from random import randrange

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = PLATFORM_LAYER
        self.groups = game.allSprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
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

        if randrange(100) < POW_SPAWN_PCT:
            Pow(game, self)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.allSprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["boost"])
        self.image = self.game.enemySpritesheet.getImage(103, 119, 44, 30)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.allSprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloudImages)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.downScale = randrange(2, 5)

        scale = randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))

        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()

