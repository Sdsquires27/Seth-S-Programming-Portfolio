import pygame
import pygame as pg
from settings import *
from tilemap import *
from random import uniform, randint, choice
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        super(Player, self).__init__()
        self.game = game
        self.image = pygame.transform.scale(game.playerImg, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hitRect = PLAYER_HIT_RECT
        self.hitRect.center = self.rect.center
        self.lastShot = 0
        self.health = PLAYER_HEALTH

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.rot = 0
        self.weapon = "pistol"

    def getKeys(self):
        self.rotSpeed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotSpeed = PLAYER_ROT_SPEED * self.game.dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotSpeed = - PLAYER_ROT_SPEED * self.game.dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.lastShot > WEAPONS[self.weapon]["rate"]:
            self.lastShot = now
            dir = vec(1, 0).rotate(-self.rot)
            bulletPos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]["kickback"], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]["count"]):
                spread = uniform(-WEAPONS[self.weapon]["spread"], WEAPONS[self.weapon]["spread"])
                Bullet(self.game, bulletPos, dir.rotate(spread))
                choice(self.game.weaponSounds[self.weapon]).play()
            MuzzleFlash(self.game, bulletPos)

    def update(self):
        self.getKeys()

        self.rot = (self.rot + self.rotSpeed + self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.playerImg, self.rot)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.pos += self.vel * self.game.dt
        self.hitRect.centerx = self.pos.x
        collideWithWalls(self, self.game.walls, "x")
        self.hitRect.centery = self.pos.y
        collideWithWalls(self, self.game.walls, "y")
        self.rect.center = self.hitRect.center

    def addHealth(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self._layer = BULLET_LAYER
        self.groups = game.allSprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.bulletImages[WEAPONS[game.player.weapon]["size"]]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * WEAPONS[game.player.weapon]["speed"]
        self.spawnTime = pg.time.get_ticks()
        self.game = game

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()

        if pg.time.get_ticks() - self.spawnTime > WEAPONS[self.game.player.weapon]["lifetime"]:
            self.kill()

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gunFlashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawnTime = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawnTime > FLASH_DURATION:
            self.kill()
