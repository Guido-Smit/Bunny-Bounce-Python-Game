import pygame as pg
import random
from Settings import *
from Sprites import *
from Functions import *
import math


class Game:
    def __init__(self):
        # initialize game
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Pikajump")
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # reset game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop updater
        self.all_sprites.update()
        #check if player hits platform
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

        # if player is 3/4 on way to top
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()


        #spawn new platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # game loop -events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        draw_text(self.screen, str(self.player.pos), 25, WIDTH / 2, 50)
        # create the display
        pg.display.flip()  # flip the screen 60 times a second

    def show_start_screen(self):
        # start menu/screen
        pass

    def show_go_screen(self):
        # Game over
        pass


g = Game()

g.show_start_screen()

while g.running:
    g.new()
    g.show_start_screen()

pg.quit()




