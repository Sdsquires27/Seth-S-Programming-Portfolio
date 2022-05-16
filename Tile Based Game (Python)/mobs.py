from settings import *
import pygame as pg
vec = pg.math.Vector2
from random import choice, random


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.allSprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mobImg.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hitRect = MOB_HIT_RECT.copy()
        self.hitRect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.speed = choice(MOB_SPEEDS)
        self.rot = 0
        self.health = MOB_HEALTH
        self.rect.center = self.pos
        self.target = self.game.player

    def update(self):
        targetDist = self.target.pos - self.pos
        if targetDist.length_squared() < DETECT_RADIUS ** 2:
            if random() < 0.002:
                choice(self.game.zombieMoanSounds).play()
            self.rot = targetDist.angle_to(vec(1, 0))

            self.image = pg.transform.rotate(self.game.mobImg.copy(), self.rot)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.avoidMobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hitRect.centerx = self.pos.x
            collideWithWalls(self, self.game.walls, "x")
            self.hitRect.centery = self.pos.y
            collideWithWalls(self, self.game.walls, "y")
            self.rect.center = self.hitRect.center
        if self.health <= 0:
            choice(self.game.zombieHitSounds).play()
            self.game.mapImg.blit(self.game.splat, self.pos - vec(32, 32))
            self.kill()

    def avoidMobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def drawHealth(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.healthBar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.healthBar)
