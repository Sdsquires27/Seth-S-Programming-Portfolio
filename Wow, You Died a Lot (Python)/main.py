# Pygame template - skeleton for a new pygame project
import pygame as pg
import random
from player import *
from platform import *
from levelData import *


class Game:
    def __init__(self):
        # initialize pygame and create window
        self.playerImg = None
        self.running = True
        self.curX = 0
        self.curY = 0
        self.curLev = 0
        self.fontName = pg.font.match_font(FONT_NAME)

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
        self.obstacles = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

        # initialize player
        self.player = Player(self)
        self.allSprites.add(self.player)

        # load level
        for plat in LEVELS[self.curLev]:
            Platform(*plat, self)

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
        # if the round hasn't ended:
        if not self.player.won or self.ghosts:
            # Game Loop - Update
            self.allSprites.update()
            # self.moveScreen()

            # col between sprite and obstacles
            hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
            if hits:
                self.player.die()

            # col between sprite and goal
            hits = pg.sprite.spritecollide(self.player, self.goal, False)
            if hits:
                if not self.player.won:
                    self.player.win()

        # if the round has ended:
        else:
            self.curLev += 1
            self.showWinScreen()
            self.new()

    def moveScreen(self):
        # if player reaches front half of the screen
        if self.player.pos.x > WIDTH * 3 / 4:
            self.curX += max(abs(self.player.vel.x), 2)
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for platform in self.platforms:
                platform.rect.x -= max(abs(self.player.vel.x), 2)


        # if player reaches back half of the screen
        if self.player.rect.left < WIDTH / 4:
            distance = max(abs(self.player.vel.x), 2)
            self.curX -= distance
            self.player.pos.x += distance
            for platform in self.platforms:
                platform.rect.x += distance

            # If you're past the very left of the screen, add back
            if self.curX < 0:
                self.curX += distance
                self.player.pos.x -= distance
                for platform in self.platforms:
                    platform.rect.x -= distance

        # if you're past at the top of the screen
        # if self.player.rect.top > HEIGHT * 3 / 4:
        #     distance = max(abs(self.player.vel.y), 2)
        #     self.curY += distance
        #     self.player.pos.y -= distance
        #     for platform in self.platforms:
        #         platform.rect.y -= distance
        #
        #
        # if self.player.rect.bottom < HEIGHT / 4:
        #     distance = max(abs(self.player.vel.y), 2)
        #     self.curY -= distance
        #     self.player.pos.y += distance
        #     for platform in self.platforms:
        #         platform.rect.y += distance
        #
        #     # If you're past the very bottom of the screen, add back
        #     if self.curY < 0:
        #         self.curY += distance
        #         self.player.pos.y -= distance
        #         for platform in self.platforms:
        #             platform.rect.y -= distance

    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP:
                    self.player.jump()

    def draw(self):
        # game loop - draw
        self.screen.fill(BLUE)
        self.allSprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def drawText(self, text, size, color, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

    def showStartScreen(self):
        # game splash/start screen
        pass

    def showWinScreen(self):
        self.screen.fill(BLUE)
        self.drawText("Level Complete!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Deaths: " + str(self.player.lifeNum), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        self.waiting = True
        while self.waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False

    def showGoScreen(self):
        # game over screen
        pass

g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGoScreen()

pygame.quit()
