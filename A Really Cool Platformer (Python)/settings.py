import os
import random

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")

WIDTH = 1600
HEIGHT = 900
FPS = 60
TITLE = "Platformer"


# define game properties
PLAYER_LAYER = 3
PLAYER_ACC = 2
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 1.5
PLAYER_JUMP = 23

PLATFORM_LAYER = 2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



