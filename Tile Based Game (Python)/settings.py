import os
import random
import pygame as pg
vec = pg.math.Vector2

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")
mapFolder = os.path.join(gameFolder, "maps")

WIDTH = 1024
HEIGHT = 768
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
BROWN = (106, 55, 5)

TITLE = "Tilemap game"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = "element_green_square.png"

#player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# gun settings
BULLET_IMG = "bullet.png"
BULLET_SPEED = 500
BULLET_LIFE = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 10
BULLET_DMG = 10

# mob settings
MOB_DAMAGE = 10
MOB_HEALTH = 100
MOB_IMAGE = "zombie1.png"
MOB_SPEED = 150
MOB_KNOCKBACK = 10
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)


def collideHitRecT(one, two):
    return one.hitRect.colliderect(two.rect)

def collideWithWalls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRecT)
        if hits:
            if hits[0].rect.centery > sprite.hitRect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitRect.width / 2.0
            if hits[0].rect.centery < sprite.hitRect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hitRect.width / 2.0
            sprite.vel.x = 0
            sprite.hitRect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRecT)
        if hits:
            if hits[0].rect.centery > sprite.hitRect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hitRect.height / 2.0
            if hits[0].rect.centery < sprite.hitRect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hitRect.height / 2.0
            sprite.vel.y = 0
            sprite.hitRect.centery = sprite.pos.y
