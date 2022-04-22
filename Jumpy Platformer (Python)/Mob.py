from settings import *
import pygame as pg
from random import choice
from random import randrange

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.allSprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.flyFrames = [self.game.enemySpritesheet.getImage(0, 32, 72, 36),
                          self.game.enemySpritesheet.getImage(0, 0, 75, 31)]
        self.flyFramesL = []
        for frame in self.flyFrames:
            frame.set_colorkey(BLACK)
            self.flyFramesL.append(pg.transform.flip(frame, True, False))

        self.image = self.flyFrames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1

        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

        self.currentFrame = 0
        self.lastUpdate = 0

    def update(self):
        center = self.rect.center
        self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1

        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

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

