import pygame
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.loadImages()
        self.image = self.standingImage
        self.rect = self.image.get_rect()

        self.walking = False
        self.jumping = False
        self.currentFrame = 0
        self.lastUpdate = 0

        self.won = False
        self.lifeData = [[[]]]
        self.frame = 0
        self.lifeNum = 0

        self.maxJumps = 2
        self.curJumps = 0

        self.spawnPos = vec(80, HEIGHT - 80)

        self.pos = (self.spawnPos.x, self.spawnPos.y)
        self.rect.midbottom = self.pos

        self.vel = vec(0, 0)

        self.acc = vec(0, 0)

    def loadImages(self):
        self.standingImage = self.game.playerSpritesheet.getImage(220, 0, 55, 75)
        self.standingImage.set_colorkey(BLACK)

        self.walkImagesR = [
            self.game.playerSpritesheet.getImage(0, 0, 55, 75),
            self.game.playerSpritesheet.getImage(55, 0, 55, 75),
            self.game.playerSpritesheet.getImage(0, 80, 55, 75),
            self.game.playerSpritesheet.getImage(55, 80, 55, 75),
            self.game.playerSpritesheet.getImage(165, 80, 55, 75),
            self.game.playerSpritesheet.getImage(220, 0, 55, 75),
            self.game.playerSpritesheet.getImage(55, 80, 55, 75),
            self.game.playerSpritesheet.getImage(0, 80, 55, 75),
            self.game.playerSpritesheet.getImage(55, 0, 55, 75),
            self.game.playerSpritesheet.getImage(0, 0, 55, 75),
            self.game.playerSpritesheet.getImage(220, 0, 55, 75)
        ]
        self.walkImagesL = []
        for frame in self.walkImagesR:
            frame.set_colorkey(BLACK)
            self.walkImagesL.append(pygame.transform.flip(frame, True, False))

        self.jumpFrameR = self.game.playerSpritesheet.getImage(165, 160, 55, 75)
        self.jumpFrameR.set_colorkey(BLACK)

        self.jumpFrameL = pygame.transform.flip(self.jumpFrameR, True, False)


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

    def die(self):
        self.pos = (self.spawnPos.x, self.spawnPos.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.lifeNum += 1
        self.lifeData.append([])

    def replayDeaths(self):
        for i in range(len(self.lifeData)):
            Ghost(self, i)

    def win(self):
        self.won = True
        self.replayDeaths()
        self.kill()

    def update(self):
        self.animate()
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

        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append((self.pos.x, self.pos.y))
        self.lifeData[self.lifeNum].append([])

    def animate(self):
        animType = "s"
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if not self.jumping and not self.walking:
            self.lastUpdate = now
            self.image = self.standingImage

        if self.jumping:
            self.lastupdate = now
            if self.vel.x > 0:
                animType = "jr"
                self.image = self.jumpFrameR
            else:
                animType = "jl"
                self.image = self.jumpFrameL

        elif self.walking:
            if self.vel.x > 0:
                animType = "wr"
            else:
                animType = "wl"

            if now - self.lastUpdate > 50:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walkImagesR)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walkImagesR[self.currentFrame]
                else:
                    self.image = self.walkImagesL[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append(animType)
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append(self.currentFrame)

class Ghost(pygame.sprite.Sprite):
    def __init__(self, player, num):
        self._layer = PLAYER_LAYER
        self.groups = player.game.allSprites, player.game.ghosts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.game = player.game
        self.image = self.player.standingImage
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.num = num
        self.frame = 0
        self.pos = self.player.lifeData[num][0][2]

        self.rect.midbottom = self.pos

    def update(self):
        self.frame += 1
        if self.frame < len(self.player.lifeData[self.num]) - 1:
            anim, animFrame, self.pos = self.player.lifeData[self.num][self.frame]
            self.rect.midbottom = self.pos

            if anim == "s":
                self.image = self.player.standingImage
            elif anim == "jr":
                self.image = self.player.jumpFrameR
            elif anim == "jl":
                self.image = self.player.jumpFrameL
            elif anim == "wr":
                self.image = self.player.walkImagesR[animFrame]
            elif anim == "wl":
                self.image = self.player.walkImagesL[animFrame]


        else:
            self.kill()
