# Pygame template - skeleton for a new pygame project
import pygame
import pygame as pg
import random
from player import *
from platform import *
from os import path
from spritesheet import *

class Game:
    def __init__(self):
        # initialize pygame and create window
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.fontName = pg.font.match_font(FONT_NAME)
        self.loadData()

    def loadData(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")

        with open(path.join(self.dir, HS_FILE), "r") as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        self.platformImageBig = pygame.image.load(os.path.join(imgFolder, "ground_grass.png"))
        self.platformImageSmall = pygame.image.load(os.path.join(imgFolder, "ground_grass_small.png"))

        # load spritesheet image
        self.playerSpritesheet = Spritesheet(path.join(img_dir, PLAYER_SPRITESHEET))

    def new(self):
        # initialize the game
        self.allSprites = pygame.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.score = 0

        # initialize player
        self.player = Player(self)
        self.allSprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(*plat, self)
            self.allSprites.add(p)
            self.platforms.add(p)

        g.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.allSprites.update()

        # check if player hits a platform and is falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.jumping = False
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0

        # if player reaches top 1 / 4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # Die!
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30),
                         self)
            self.platforms.add(p)
            self.allSprites.add(p)

    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jumpCut()

    def draw(self):
        # game loop - draw
        self.screen.fill(LIGHTBLUE)
        self.allSprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        # draw score
        self.drawText(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def showStartScreen(self):
        # game splash/start screen
        self.screen.fill(LIGHTBLUE)
        self.drawText("Jumpy platformer", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Arrow keys to move, space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press any key to start", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.drawText("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.waitForKey()

    def showGoScreen(self):
        # game over screen
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.drawText("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Score: "+ str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Pres a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        if self.score > self.highscore:
            self.highscore = self.score
            self.drawText("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
            self.drawText("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.waitForKey()

    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def drawText(self, text, size, color, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGoScreen()

pygame.quit()
