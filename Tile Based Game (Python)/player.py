import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super(Player, self).__init__()
        self.game = game
        self.image = pygame.transform.scale(game.playerImg, (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if not self.collideWithWalls(dx, dy):
            self.x += dx
            self.y += dy

    def collideWithWalls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False


    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0