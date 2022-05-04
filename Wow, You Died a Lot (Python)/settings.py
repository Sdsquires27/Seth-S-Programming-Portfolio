import os
import pygame as pg

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")

# project properties
WIDTH = 1600
HEIGHT = 900
FPS = 60
TITLE = "Wow, you died a lot"
FONT_NAME = "varino"
LEVEL_FILE = "level.txt"

PLAYER_SPRITESHEET = os.path.join(imgFolder, "player.png")

JUMP = pg.K_SPACE

# define game properties
PLAYER_LAYER = 3
PLAYER_ACC = 2
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 1.5
PLAYER_JUMP = 23

PLATFORM_LAYER = 2

UI_LAYER = 3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
