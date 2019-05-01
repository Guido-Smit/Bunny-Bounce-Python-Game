import pygame as pg
import random
#setup

TITLE = "Pikajump"
WIDTH = 600
HEIGHT = 800
FPS = 60


font_name = pg.font.match_font("Arial")

#Starting Platforms

PLATFORM_LIST = [(0, HEIGHT - 20, WIDTH, 50),
                 (random.randrange(0, WIDTH), HEIGHT - 120, random.randrange(10, WIDTH/2), 10),
                 (random.randrange(0, WIDTH), HEIGHT - 250, random.randrange(10, WIDTH/2), 10),
                 (random.randrange(0, WIDTH), HEIGHT - 320, random.randrange(10, WIDTH/2), 10),
                 (random.randrange(0, WIDTH), HEIGHT - 450, random.randrange(10, WIDTH/2), 10),
                 (random.randrange(0, WIDTH), HEIGHT - 650, random.randrange(10, WIDTH/2), 10),


                 ]

#player properties
PLAYER_ACC = 0.5
PLAYER_FRIC = -0.12
MINIMAL_VEL = 0.001
JUMPSPEED = 20
GRAVITY = 0.75

#colours
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)