import pygame as pg
import random
from Settings import *
from Sprites import *
from os import path
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
        self.font_name = pg.font.match_font(font_name)
        self.load_data()


    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "Artwork", "Spritesheets")

        try:
            with open(path.join(self.dir, HS_FILE), "r+") as f:
                    self.highscore = int(f.read())
        except:
            with open(path.join(self.dir, HS_FILE), "w"):
                    self.highscore = 0

        # load spritesheets
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        # reset game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
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
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y <= lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top +1
                    self.player.vel.y = 0
                    self.player.jumping = False

        # if player is 3/4 on way to top
        if self.player.rect.top <= HEIGHT/4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        #Game Over
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0 :
                   sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False



        #spawn new platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()


    def draw(self):
        # game loop draw
        self.screen.fill(BG_COLOUR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # create the display
        pg.display.flip()  # flip the screen 60 times a second

    def show_start_screen(self):
        # start menu/screen
        self.screen.fill(BG_COLOUR)
        self.draw_text(TITLE, 90, YELLOW, WIDTH / 2, HEIGHT * 1 / 4)
        self.draw_text("Arrow keys for movement, spacebar to jump", 35, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play", 30, YELLOW, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score = " + str(self.highscore), 30, YELLOW, WIDTH / 2, HEIGHT * 3 / 5)
        pg.display.flip()
        self.wait_for_key_input()


    def show_go_screen(self):
        # Game over
        if not self.running:
            return
        self.screen.fill(BG_COLOUR)
        self.draw_text("Game Over", 90, YELLOW, WIDTH / 2, HEIGHT * 1 / 4)
        self.draw_text("Score = " + str(self.score), 35, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 30, YELLOW, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 5)
            with open(path.join(self.dir,HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score = " + str(self.highscore), 30, YELLOW, WIDTH / 2, HEIGHT * 3 / 5)

        pg.display.flip()
        self.wait_for_key_input()


    def wait_for_key_input(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self, text, size, colour,  x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()

g.show_start_screen()

while g.running:
    g.new()
    g.show_go_screen()

pg.quit()




