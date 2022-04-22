# Pygame template - skeleton for a new pygame project
import pygame as pg
import random
from player import *

class Game():
    def __init__(self):
        # initialize pygame and create window
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()

    def new(self):
        # initialize the game
        self.allSprites = pygame.sprite.Group()

        # initialize player
        playerImg = pg.image.load(os.path.join(imgFolder, "Vessel.png")).convert()
        player = Player(playerImg)
        self.allSprites.add(player)

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

    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

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
