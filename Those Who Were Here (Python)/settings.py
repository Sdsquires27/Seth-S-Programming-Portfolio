import os
import random

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")
lvlFolder = os.path.join(gameFolder, "levels")

PLAYER_SPRITESHEET = os.path.join(imgFolder, "player.png")
TILES_SPRITESHEET = os.path.join(imgFolder, "tiles_spritesheet.png")

WIDTH = 1600
HEIGHT = 960
FPS = 60
TITLE = "Those Who Were Here"
fontname = "helvetica"
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# define game properties
PLAYER_LAYER = 3
PLAYER_ACC = 2
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 1.5
PLAYER_JUMP = 23

PLATFORM_LAYER = 2
UI_LAYER = 5
SWITCH_LAYER = 1

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)

LEVEL_FILE = "level.txt"


