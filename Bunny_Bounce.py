# Credits

# https://opengameart.org/content/oldschool-win-and-die-jump-and-run-sounds


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
        pg.display.set_caption("Bunny Bounce")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(font_name)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        all_imgs = path.join(self.dir, "Artwork")
        img_dir = path.join(self.dir, "Artwork", "Spritesheets")

        try:
            with open(path.join(self.dir, HS_FILE), "r+") as f:
                self.highscore = int(f.read())
        except:
            with open(path.join(self.dir, HS_FILE), "w"):
                self.highscore = 0

        # load spritesheets
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.openingbunny = pg.image.load(path.join(all_imgs, "PNG", "Background", "intro1.png"))
        self.smallerbunny = pg.transform.scale(self.openingbunny,(WIDTH, int(HEIGHT/2)))

        # clouds
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join
                                                   (all_imgs, "PNG", "Background", "cloud{}.png".
                                                    format(i))).convert_alpha())

        # load sounds
        self.sound_dir = path.join(self.dir, "Sounds")
        self.jump_sound = pg.mixer.Sound(path.join(self.sound_dir, "jump_02.wav"))
        self.death_sound = pg.mixer.Sound(path.join(self.sound_dir, "death.wav"))
        pg.mixer_music.load(path.join(self.sound_dir, "jump and run - tropics.ogg"))
        self.powerup_sound = pg.mixer.Sound(path.join(self.sound_dir, "powerup.wav"))

    def new(self):
        # reset game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        for i in range(4):
            c = Cloud(self)
            c.rect.y += 500
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

        # Mob Spawning
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # Player-Mob Collision Checking
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False
            self.death_sound.play()
            self.player.alive = False

        # Player-Platform Collision checking
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if lowest.rect.right + 10 > self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y <= lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        # Background Scrolling
        if self.player.rect.top <= HEIGHT / 4:
            if random.randrange(100) < 2:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Powerup collection
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            self.powerup_sound.play()
            if pow.type == "boost":
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # Game Over Criteria + Actions
        if self.player.rect.bottom > HEIGHT + 10:
            if self.player.alive == True:
                self.death_sound.play()
                self.player.alive = False
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False

        # Platform Spawner
        height = HEIGHT
        for platform in self.platforms:
            if platform.rect.y < height:
                height = platform.rect.y
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)


            Platform(self, random.randrange(0, WIDTH - width),
                     height - 200)

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
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        #self.draw_text(str(self.player.vel.y), 22, WHITE, WIDTH / 2, 40)

        # create the display
        pg.display.flip()  # flip the screen 60 times a second

    def show_start_screen(self):
        # start menu/screen
        pg.mixer_music.play(loops=-1)
        self.screen.fill(BG_COLOUR)
        self.screen.blit(self.smallerbunny,(0, HEIGHT/ 2))
        self.draw_text(TITLE, 90, YELLOW, WIDTH / 2, HEIGHT * 1 / 4)
        self.draw_text("Arrow keys for movement, spacebar to jump", 35, RED, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press enter to play", 30, YELLOW, WIDTH / 2, HEIGHT * 3 / 4)
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
        self.draw_text("Press enter to play again", 30, YELLOW, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, BLUE, WIDTH / 2, HEIGHT * 3 / 5)
            with open(path.join(self.dir, HS_FILE), "w") as f:
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
                    if event.key == pg.K_RETURN:
                        waiting = False

    def draw_text(self, text, size, colour, x, y):
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
