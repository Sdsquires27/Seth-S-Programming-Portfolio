# Pygame template - skeleton for a new pygame project
import pygame as pg
import random
from os import path
from player import *
from wall import *

class Game():
    def __init__(self):
        # initialize pygame and create window
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()
        pg.key.set_repeat(500, 100)

    def loadData(self):
        self.allSprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.mapData = []
        with open(path.join(gameFolder, "map.txt"), "rt") as f:
            for line in f:
                self.mapData.append(line)


        # initialize player
        self.playerImg = pg.image.load(os.path.join(imgFolder, "Vessel.png")).convert()

    def new(self):
        # initialize the game

        for row, tiles in enumerate(self.mapData):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    self.player = Player(self, col, row)
                    self.allSprites.add(self.player)

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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, GREEN, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, GREEN, (0, y), (WIDTH, y))

    def draw(self):
        # game loop - draw
        self.screen.fill(BGCOLOR)
        self.allSprites.draw(self.screen)
        self.drawGrid()
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
