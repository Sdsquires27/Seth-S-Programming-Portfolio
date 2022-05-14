import pygame.sprite

from settings import *
import pygame as pg
vec = pg.math.Vector2


class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self._layer -= 1
        self.groups = game.allSprites, game.objects, game.boxes, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.transform.scale(game.tilesSpritesheet.getImage(0, 792, 70, 70), (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

        self.game = game

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.y += self.rect.height
        self.x += self.rect.width / 2

        self.pos = vec(self.x, self.y)
        self.spawnPos = vec(self.pos.x, self.pos.y)

        self.rect.midbottom = self.pos

        self.vel = vec(0, 0)

        self.acc = vec(0, 0)

        self.held = False
        self.holder = None

    def update(self):
        if self.held:
            self.rect.midbottom = self.holder.rect.midtop

        else:
            # apply friction
            self.acc = vec(0, PLAYER_GRAV)

            self.acc.x += self.vel.x * PLAYER_FRICTION

            # equations of motion
            self.vel += self.acc
            if abs(self.vel.x) < 0.1:
                self.vel.x = 0
            self.pos += self.vel + 0.5 * self.acc

            # move player to position
            self.rect.centerx = self.pos.x

            hits = []
            for platform in self.game.platforms:
                if platform != self:
                    if pygame.sprite.collide_rect(self, platform):
                        hits.append(platform)
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

            # accounting for collisions
            hits = []
            for platform in self.game.platforms:
                if platform != self:
                    if pygame.sprite.collide_rect(self, platform):
                        hits.append(platform)
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

    def pickUp(self, holder):
        self.held = True
        self.holder = holder
        if self.holder == self.game.player:
            self.game.platforms.remove(self)

    def reset(self):
        self.held = False
        self.holder = None
        self.pos = self.spawnPos
        self.vel = vec(0, 0)
        self.spawnPos = vec(self.pos.x, self.pos.y)
        self.game.platforms.add(self)


    def drop(self, moving, direction):
        self.held = False
        if moving:
            self.pos = self.rect.center
            self.vel = vec(75, -1)
            self.vel.x *= direction
        else:
            if direction == 1:
                direction = 2
            self.pos.x = self.rect.x
            self.pos.x += TILESIZE * direction
            self.rect.centerx = self.pos.x
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            if hits:
                self.pos.x -= TILESIZE * 2 * direction
        self.game.platforms.add(self)
