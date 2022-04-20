import os
import random

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")

HS_FILE = "highscore.txt"

PLAYER_SPRITESHEET = "p1_spritesheet.png"
ENEMY_SPRITESHEET = "enemies_spritesheet.png"

# project properties
WIDTH = 480
HEIGHT = 600
FPS = 60
TITLE = "Jumpy Platformer"
FONT_NAME = "helvetica"

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH/2 - 50, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.15
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 155, 155)



