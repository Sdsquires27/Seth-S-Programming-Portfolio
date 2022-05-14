from settings import *
import pygame as pg

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile):
        self._layer = PLATFORM_LAYER
        self.groups = game.allSprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        if tile == "1":
            # normal grass
            self.image = pg.transform.scale(game.tilesSpritesheet.getImage(504, 576, 70, 70), (TILESIZE, TILESIZE))
        elif tile == "2":
            # empty dirt
            self.image = pg.transform.scale(game.tilesSpritesheet.getImage(576, 864, 70, 70), (TILESIZE, TILESIZE))
        elif tile == "3":
            # hill left
            self.image = pg.transform.scale(game.tilesSpritesheet.getImage(576, 576, 70, 70), (TILESIZE, TILESIZE))
        elif tile == "4":
            # hill right
            self.image = pg.transform.scale(game.tilesSpritesheet.getImage(576, 720, 70, 70), (TILESIZE, TILESIZE))
        elif tile == "0":
            # spikes
            self.image = pg.transform.scale(game.spikeImage, (TILESIZE, TILESIZE))
            self.image.set_colorkey(BLACK)
            self.game.obstacles.add(self)
            self.game.platforms.remove(self)
        elif tile == "9":
            # upside down spikes
            self.image = pg.transform.scale(game.spikeImage, (TILESIZE, TILESIZE))
            self.image = pg.transform.rotate(self.image, 180)
            self.image.set_colorkey(BLACK)
            self.game.obstacles.add(self)
            self.game.platforms.remove(self)

        elif tile == "G":
            self.closedImage = pg.transform.scale(game.tilesSpritesheet.getImage(648, 432, 70, 70), (TILESIZE, TILESIZE))
            self.game.goal.add(self)
            self.game.platforms.remove(self)
            self.openImage = pg.transform.scale(game.tilesSpritesheet.getImage(648, 288, 70, 70), (TILESIZE, TILESIZE))
            self.image = self.closedImage

        elif tile == "g":
            self.closedImage = pg.transform.scale(game.tilesSpritesheet.getImage(648, 360, 70, 70), (TILESIZE, TILESIZE))
            self.game.goal.add(self)
            self.game.platforms.remove(self)
            self.openImage = pg.transform.scale(game.tilesSpritesheet.getImage(648, 216, 70, 70), (TILESIZE, TILESIZE))
            self.image = self.closedImage

        self.tile = tile.upper()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        if self.tile == "G":
            if self.game.doorOpen:
                self.image = self.openImage
            else:
                self.image = self.closedImage