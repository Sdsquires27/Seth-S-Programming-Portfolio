import pygame
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Player, self).__init__()
        self.game = game
        self.image = pygame.transform.scale(game.playerImg, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def getKeys(self):
        self.rotSpeed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotSpeed = PLAYER_ROT_SPEED * self.game.dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotSpeed = - PLAYER_ROT_SPEED* self.game.dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)

    def collideWithWalls(self, dir):
        if dir == "x":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.centerx = self.pos.x
        if dir == "y":
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom / 2
                self.vel.y = 0
                self.rect.centery = self.pos.y


    def update(self):
        self.getKeys()

        self.rot = (self.rot + self.rotSpeed + self.game.dt) % 360
        self.image = pygame.transform.rotate(self.game.playerImg, self.rot)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.pos += self.vel * self.game.dt
        self.rect.centerx = self.pos.x
        self.collideWithWalls("x")
        self.rect.centery = self.pos.y
        self.collideWithWalls("y")
