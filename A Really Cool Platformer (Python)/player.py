import pygame
from settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.playerImg
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.jumping = False

        self.maxJumps = 2
        self.curJumps = 0

        self.pos = vec(80, HEIGHT - 80)
        self.rect.midbottom = self.pos

        self.vel = vec(0, 0)

        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        if self.curJumps > 0:
            self.vel.y = -PLAYER_JUMP
            self.curJumps -= 1
            self.jumping = True

    def isOnGround(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        return hits

    def update(self):
        if self.isOnGround() and not self.jumping:
            self.curJumps = self.maxJumps

        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # move player to position
        self.rect.centerx = self.pos.x

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            for hit in hits:
                if self.vel.x > 0:
                    if self.pos.x + self.rect.width / 2 > hit.rect.left:
                        self.pos.x = hit.rect.left - self.rect.width / 2
                        self.vel.x = 0

                elif self.vel.x < 0:
                    if self.pos.x - self.rect.width / 2 < hit.rect.right:
                        self.pos.x = hit.rect.right + self.rect.width / 2
                        self.vel.x = 0
        self.rect.centerx = self.pos.x


        self.rect.bottom = self.pos.y

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            for hit in hits:
                if self.vel.y > 0:
                    if self.pos.y > hit.rect.top:
                        self.pos.y = hit.rect.top
                        self.vel.y = 0
                        self.jumping = False

                elif self.vel.y < 0:
                    if self.pos.y + self.rect.height > hit.rect.bottom:
                        self.pos.y = hit.rect.bottom + self.rect.height
                        self.vel.y = 0

        self.rect.bottom = self.pos.y
