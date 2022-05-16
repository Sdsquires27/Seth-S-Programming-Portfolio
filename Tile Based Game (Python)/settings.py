import os
import random
import pygame as pg
vec = pg.math.Vector2

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")
mapFolder = os.path.join(gameFolder, "maps")
sndFolder = os.path.join(gameFolder, "snd")

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
WALL_LAYER = 1

# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
PLAYER_LAYER = 2

# gun settings
BULLET_IMG = "bullet.png"
WEAPONS = {}
WEAPONS["pistol"] = {"speed": 500,
                     "lifetime": 1000,
                     "rate": 250,
                     "kickback": 200,
                     "spread": 5,
                     "damage": 10,
                     "size": "lg",
                     "count": 1}
WEAPONS["shotgun"] = {"speed": 400,
                      "lifetime": 500,
                      "rate": 900,
                      "kickback": 300,
                      "spread": 20,
                      "damage": 5,
                      "size": "sm",
                      "count": 12}

# BULLET_SPEED = 500
# BULLET_LIFE = 1000
# BULLET_RATE = 150
# KICKBACK = 200
# GUN_SPREAD = 10
# BULLET_DMG = 10
BULLET_LAYER = 3

# mob settings
MOB_DAMAGE = 10
MOB_HEALTH = 100
MOB_IMAGE = "zombie1.png"
MOB_SPEEDS = [150, 200, 100, 150, 125]
MOB_KNOCKBACK = 10
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
AVOID_RADIUS = 50
MOB_LAYER = 2
DETECT_RADIUS = 400
SPLAT = "splat green.png"

# game effects
MUZZLE_FLASHES = ["whitePuff15.png", "whitePuff16.png", "whitePuff17.png", "whitePuff18.png"]
FLASH_DURATION = 40
EFFECTS_LAYER = 4
DAMAGE_ALPHA = [i for i in range(0, 255, 25)]

# items
ITEM_IMAGES = {"health": "health_pack.png",
               "shotgun": "obj_shotgun.png"}
ITEM_LAYER = 1
HEALTH_PACK_AMOUNT = 30
BOB_RANGE = 20
BOB_SPEED = 0.6

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']

WEAPON_SOUNDS = {"pistol": ["pistol.wav"],
                 "shotgun": ["shotgun.wav"]}

EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  "gunPickup": "gun_pickup.wav"}

def collideHitRecT(one, two):
    return one.hitRect.colliderect(two.rect)

def collideWithWalls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collideHitRecT)
        if hits:
            if hits[0].rect.centerx > sprite.hitRect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hitRect.width / 2.0
            if hits[0].rect.centerx < sprite.hitRect.centerx:
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
