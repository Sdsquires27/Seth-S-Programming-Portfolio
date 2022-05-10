from settings import *
import pygame as pg
from random import choice
from random import randrange


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, xMin, xMax, y, speed):
        self._layer = ENEMY_LAYER
        self.groups = game.allSprites, game.obstacles, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.xMax = xMax
        self.xMin = xMin
        self.start = xMin
        if self.xMin > self.xMax:
            var = self.xMin
            self.xMin = self.xMax
            self.xMax = var

        self.flyFrames = [self.game.enemySpritesheet.getImage(0, 32, 72, 36),
                          self.game.enemySpritesheet.getImage(0, 0, 75, 31)]
        self.flyFramesL = []
        for frame in self.flyFrames:
            frame.set_colorkey(BLACK)
            self.flyFramesL.append(pg.transform.flip(frame, True, False))

        self.image = self.flyFrames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.start

        self.vx = speed

        self.y = y
        self.rect.centery = y
        self.vy = 0
        self.dy = 0.5

        self.currentFrame = 0
        self.lastUpdate = 0

    def reset(self):
        self.rect.center = (self.start, self.y)
        self.vx = abs(self.vx)


    def update(self):
        center = self.rect.center
        self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -2.9:
            self.dy *= -1

        self.rect.y += self.vy
        if self.rect.left > self.xMax or self.rect.right < self.xMin:
            self.vx *= -1

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.lastUpdate > 100:
            self.lastUpdate = now
            self.currentFrame = (self.currentFrame + 1) % len(self.flyFrames)
            if self.vx > 0:
                self.image = self.flyFramesL[self.currentFrame]
            else:
                self.image = self.flyFrames[self.currentFrame]
        self.mask = pg.mask.from_surface(self.image)

