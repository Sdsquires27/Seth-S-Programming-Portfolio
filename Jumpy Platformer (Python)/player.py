import pygame
from settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.currentFrame = 0
        self.lastUpdate = 0
        self.loadImages()
        self.image = self.standingImage
        self.rect = self.image.get_rect()

        self.pos = vec(40, HEIGHT - 80)
        self.rect.midbottom = self.pos

        self.vel = vec(0, 0)

        self.acc = vec(0, 0)

    def loadImages(self):
        self.standingImage = self.game.playerSpritesheet.getImage(0, 196, 66, 92)
        self.standingImage.set_colorkey(BLACK)

        self.walkFramesR = [self.game.playerSpritesheet.getImage(0, 0, 72, 97),
                            self.game.playerSpritesheet.getImage(73, 0, 72, 97),
                            self.game.playerSpritesheet.getImage(146, 0, 72, 97),
                            self.game.playerSpritesheet.getImage(0, 98, 72, 97),
                            self.game.playerSpritesheet.getImage(73, 98, 72, 97),
                            self.game.playerSpritesheet.getImage(146, 98, 72, 97),
                            self.game.playerSpritesheet.getImage(219, 0, 72, 97),
                            self.game.playerSpritesheet.getImage(292, 0, 72, 97),
                            self.game.playerSpritesheet.getImage(219, 98, 72, 97),
                            self.game.playerSpritesheet.getImage(365, 0, 72, 97),
                            self.game.playerSpritesheet.getImage(292, 98, 72, 97)]

        self.walkFramesL = []
        for frame in self.walkFramesR:
            frame.set_colorkey(BLACK)
            self.walkFramesL.append(pygame.transform.flip(frame, True, False))

        self.jumpFrameR = self.game.playerSpritesheet.getImage(438, 93, 67, 94)
        self.jumpFrameR.set_colorkey(BLACK)

        self.jumpFrameL = pygame.transform.flip(self.jumpFrameR, True, False)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            self.game.jumpSnd.play()

    def jumpCut(self):
        if self.jumping:
            if self.vel.y < -7:
                self.vel.y = -7

    def update(self):
        self.animate()
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
        self.rect.midbottom = self.pos

        # wrap around screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if not self.jumping and not self.walking:
            self.lastUpdate = now
            self.image = self.standingImage

        if self.walking:
            if now - self.lastUpdate > 50:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walkFramesR)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walkFramesR[self.currentFrame]
                else:
                    self.image = self.walkFramesL[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)
