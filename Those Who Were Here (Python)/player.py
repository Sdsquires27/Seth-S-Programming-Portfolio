import pygame
from settings import *
vec = pygame.math.Vector2
from math import hypot

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.allSprites, game.objects
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.loadImages()
        self.image = self.standingImage
        self.rect = self.image.get_rect()
        self.jumping = False
        self.box = None
        self.actionPerformed = False

        self.lastSpawnTime = 0
        self.spawnNum = 0

        self.lifeData = [[[]]]
        self.lifeNum = 0

        self.currentFrame = 0

        self.maxJumps = 2
        self.curJumps = 0

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.y += self.rect.height
        self.x += self.rect.width / 2

        self.pos = vec(self.x, self.y)

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

    def loadImages(self):
        self.standingImage = self.game.playerSpritesheet.getImage(220, 0, 55, 80)
        # self.standingImage.set_colorkey(BLACK)

        self.walkImagesR = [
            self.game.playerSpritesheet.getImage(0, 0, 55, 80),
            self.game.playerSpritesheet.getImage(55, 0, 55, 80),
            self.game.playerSpritesheet.getImage(0, 80, 55, 80),
            self.game.playerSpritesheet.getImage(55, 80, 55, 80),
            self.game.playerSpritesheet.getImage(165, 80, 55, 80),
            self.game.playerSpritesheet.getImage(220, 0, 55, 80),
            self.game.playerSpritesheet.getImage(55, 80, 55, 80),
            self.game.playerSpritesheet.getImage(0, 80, 55, 80),
            self.game.playerSpritesheet.getImage(55, 0, 55, 80),
            self.game.playerSpritesheet.getImage(0, 0, 55, 80),
            self.game.playerSpritesheet.getImage(220, 0, 55, 80)
        ]
        self.walkImagesL = []
        for frame in self.walkImagesR:
            # frame.set_colorkey(BLACK)
            self.walkImagesL.append(pygame.transform.flip(frame, True, False))

        self.jumpFrameR = self.game.playerSpritesheet.getImage(165, 160, 55, 80)
        # self.jumpFrameR.set_colorkey(BLACK)

        self.jumpFrameL = pygame.transform.flip(self.jumpFrameR, True, False)

    def animate(self):
        self.animType = "s"
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
                self.animType = "jr"
                self.image = self.jumpFrameR
            else:
                self.animType = "jl"
                self.image = self.jumpFrameL

        elif self.walking:
            if self.vel.x > 0:
                self.animType = "wr"
            else:
                self.animType = "wl"

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

    def spawnGhost(self):
        Ghost(self, self.spawnNum)
        self.spawnNum += 1

    def reset(self):
        self.die()
        self.lifeData = [[[]]]
        self.lifeNum = 0

    def update(self):
        self.animate()

        # spawning
        # if there are still ghosts to spawn, spawn the ghosts
        if self.spawnNum < self.lifeNum:
            now = pygame.time.get_ticks()
            self.lastSpawnTime += 1
            if now - self.lastSpawnTime > 1200:
                self.lastSpawnTime = now
                self.spawnGhost()


        # jumps
        if self.isOnGround() and not self.jumping:
            self.curJumps = self.maxJumps

        # moving
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

        # accounting for collisions
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

        # interactions
        keyDown = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.actionPerformed:
                keyDown = True
                self.actionPerformed = True
                if self.box:
                    moving = False
                    if abs(self.vel.x) > 4:
                        moving = True
                    direction = 1
                    if self.vel.x < 0:
                        direction = -1
                    self.box.drop(moving, direction)
                    self.box = None
                else:
                    for box in self.game.boxes:
                        dist = hypot(self.rect.x - box.rect.x, self.rect.y - box.rect.y)
                        if dist < 100:
                            self.box = box
                            box.pickUp(self)
        else:
            self.actionPerformed = False

        if self.box:
            self.box.rect.midbottom = self.rect.midtop

        # updating position list
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append(self.animType)
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append(self.currentFrame)
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append((self.pos.x, self.pos.y))
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append(keyDown)
        self.lifeData[self.lifeNum][len(self.lifeData[self.lifeNum]) - 1].append((self.vel.x, self.vel.y))
        self.lifeData[self.lifeNum].append([])

    def die(self):
        self.pos = vec(self.x, self.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.spawnNum = 0
        self.lastSpawnTime = pygame.time.get_ticks()

        self.lifeData.append([])
        self.lifeNum += 1
        self.lifeData[self.lifeNum].append([])

        self.box = None

        for box in self.game.boxes:
            box.reset()

        for ghost in self.game.ghosts:
            ghost.kill()


class Ghost(pygame.sprite.Sprite):
    def __init__(self, player, num):
        self._layer = PLAYER_LAYER
        self.groups = player.game.allSprites, player.game.ghosts, player.game.objects
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player = player
        self.game = player.game
        self.image = self.player.standingImage
        self.rect = self.image.get_rect()
        self.num = num
        self.frame = 0
        self.vel = vec(0, 0)
        self.pos = self.player.lifeData[num][0][2]
        self.box = None

        self.rect.midbottom = self.pos

    def update(self):
        self.frame += 1
        if self.frame < len(self.player.lifeData[self.num]) - 1:
            anim, animFrame, self.pos, interact, self.vel = self.player.lifeData[self.num][self.frame]
            self.rect.midbottom = self.pos
            self.vel = vec(self.vel)

            # set animation to current player animation
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

            # gray out image
            newImage = pygame.transform.scale(self.image, (self.image.get_width(), self.image.get_height()))
            color = GREY

            colorImage = pygame.Surface(newImage.get_size()).convert_alpha()
            colorImage.fill(color)

            newImage.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            self.image = newImage

            # pick up box
            if interact:
                if self.box:
                    moving = False
                    if abs(self.vel.x) > 4:
                        moving = True
                    direction = 1
                    if self.vel.x < 0:
                        direction = -1
                    self.box.drop(moving, direction)
                    self.box = None
                else:
                    for box in self.game.boxes:
                        dist = hypot(self.rect.x - box.rect.x, self.rect.y - box.rect.y)
                        if dist < 100:
                            self.box = box
                            box.pickUp(self)


        else:
            if self.box:
                moving = False
                if abs(self.vel.x) > 4:
                    moving = True
                direction = 1
                if self.vel.x < 0:
                    direction = -1
                self.box.drop(moving, direction)
            self.kill()
