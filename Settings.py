import pygame as pg
import random
# setup

TITLE = "Bunny Bounce"
WIDTH = 600
HEIGHT = 800
FPS = 60
font_name = pg.font.match_font("Arial")
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"


# Game Properties

BOOST_POWER = 40
POW_SPAWN_CHANCE = 10
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0


# Starting Platforms

PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH * 1 / 4, HEIGHT * 3 / 4),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)
                 ]

# player properties
PLAYER_ACC = 0.6
PLAYER_FRIC = -0.12
MINIMAL_VEL = 0.1
MAXIMAL_VEL_DOWN = 14
MAXIMAL_VEL_UP = 500
JUMPSPEED = 22
GRAVITY = 0.7

# colours
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)

# The background colour
BG_COLOUR = LIGHTBLUE