# Pygame template - skeleton for a new pygame project
import pygame as pg
import random
from player import *
from platform import *

class Game():
    def __init__(self):
        # initialize pygame and create window
        self.running = True
        self.curX = 0
        self.curY = 0

        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.loadData()
        self.player = None

    def loadData(self):
        self.playerImg = pg.image.load(os.path.join(imgFolder, "Vessel.png")).convert()

    def new(self):
        # initialize the game
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()

        # initialize player
        self.player = Player(self)
        self.allSprites.add(self.player)

        Platform(0, HEIGHT - 40, self, WIDTH, 40)
        Platform(0, 0, self, 40, HEIGHT)
        Platform(0, 0, self, WIDTH, 40)

        self.curX = 0
        self.curY = 0

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

        # if player reaches front half of the screen
        if self.player.pos.x > WIDTH * 3 / 4:
            self.curX += max(abs(self.player.vel.x), 2)
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for platform in self.platforms:
                platform.rect.x -= max(abs(self.player.vel.x), 2)

        if self.player.rect.left < WIDTH / 4:
            distance = max(abs(self.player.vel.x), 2)
            self.curX -= distance
            self.player.pos.x += distance
            for platform in self.platforms:
                platform.rect.x += distance
            # If you're past the very right of the screen
            if self.curX < 0:
                self.curX += distance
                self.player.pos.x -= distance
                for platform in self.platforms:
                    platform.rect.x -= distance


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

    def draw(self):
        # game loop - draw
        self.screen.fill(BLUE)
        self.allSprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def showStartScreen(self):
        # game splash/start screen
        pass

    def showGoScreen(self):
        # game over screen
        pass

g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGoScreen()

pygame.quit()
