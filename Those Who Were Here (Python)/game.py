import pygame as pg
import random
from player import *
from platform import *
from map import *
from spritesheet import *
from button import *
from switch import *
from box import *

class Game():
    def __init__(self):
        # initialize pygame and create window
        self.running = True
        self.playing = False
        self.player = None
        self.unlockedLevel = 0

        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.fontName = pg.font.match_font(fontname)
        self.loadData()

    def loadData(self):
        self.dir = os.path.dirname(__file__)

        self.playerSpritesheet = Spritesheet(PLAYER_SPRITESHEET)
        self.tilesSpritesheet = Spritesheet(TILES_SPRITESHEET)

        self.spikeImage = pygame.image.load(os.path.join(imgFolder, "spikes.png")).convert()

        self.pushButtonUp = pygame.image.load(os.path.join(imgFolder, "pushButtonUp.png")).convert()
        self.pushButtonDown = pygame.image.load(os.path.join(imgFolder, "pushButtonDown.png")).convert()

        self.buttonImages = [pg.image.load(os.path.join(imgFolder, "button.jpg")).convert(),
                             pg.image.load(os.path.join(imgFolder, "selButton.jpg")).convert()]

        self.map = Map(lvlFolder)
        self.curLvl = 0

        # set up each of the groups that will be used for this project
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.switches = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()

        with open(os.path.join(self.dir, LEVEL_FILE), "r") as f:
            try:
                self.unlockedLevel = int(f.read())
            except:
                self.unlockedLevel = 0
        print(self.unlockedLevel)

    def new(self):
        # initialize the game
        print(self.unlockedLevel)
        self.showMenuScreen()

        self.loadLevel()

        self.doorOpen = True

        self.run()

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, GREEN, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, GREEN, (0, y), (WIDTH, y))

    def run(self):
        # Game loop
        if self.running:
            self.playing = True
            while self.playing:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()

    def update(self):
        # Game Loop - Update
        self.allSprites.update()

        # obstacle collisions
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        if hits:
            self.player.die()

        hits = pg.sprite.spritecollide(self.player, self.ghosts, False)
        if hits:
            self.player.die()

        # goal collisions
        if self.doorOpen:
            hits = pg.sprite.spritecollide(self.player, self.goal, False)
            if hits:
                self.curLvl += 1
                if self.curLvl > self.unlockedLevel:
                    print("new level unlocked")
                    self.unlockedLevel = self.curLvl
                    with open(os.path.join(self.dir, LEVEL_FILE), "w") as f:
                        f.write(str(self.unlockedLevel))

                self.showWinScreen()
                if self.running:
                    self.newLevel()

        # check if switches are all activated
        self.doorOpen = True
        for switch in self.switches:
            if not switch.selected:
                self.doorOpen = False


    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pg.K_UP:
                    if self.player:
                        self.player.jump()
                elif event.key == pg.K_z:
                    if self.player:
                        self.player.reset()

    def loadLevel(self):
        # load level
        for row, tiles in enumerate(self.map.maps[self.curLvl]):
            for col, tile in enumerate(tiles):
                if tile.isnumeric():
                    Platform(self, col, row, tile)
                elif tile == "P":
                    self.player = Player(self, col, row)
                    self.allSprites.add(self.player)
                elif tile == "G" or tile == "g":
                    Platform(self, col, row, tile)
                elif tile == "S":
                    Switch(self, col, row)
                elif tile == "B":
                    Box(self, col, row)

    def newLevel(self):
        # for calling up new level

        # delete all sprites
        for sprite in self.allSprites:
            sprite.kill()

        self.loadLevel()


        # reset player

        self.run()

    def draw(self):
        # game loop - draw
        self.screen.fill(GREY)
        self.allSprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def showStartScreen(self):
        # game splash/start screen
        self.screen.fill(GREY)
        self.drawText("Those Who Were Here", 60, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Arrow keys to move, up to jump. Press twice to double jump. Space to interact.", 30, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("This place is haunted by the ghosts who came before. They will kill you if you touch them, but they can help you, too.", 30, WHITE, WIDTH / 2, HEIGHT * 4 / 6)
        self.drawText("Press any key to start", 40, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
        pg.display.flip()

        self.waiting = True
        while self.waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    self.waiting = False

    def exitMenuScreen(self, level):
        # pass into button
        self.waiting = False
        self.curLvl = level
        for ui in self.ui:
            ui.kill()

    def showMenuScreen(self):
        # delete any buttons that might already exist
        for ui in self.ui:
            ui.kill()

        for i in range(len(self.map.maps)):
            if self.unlockedLevel >= i:
                function = lambda i2=i: self.exitMenuScreen(i2)
            else:
                function = None
            Button(self, (WIDTH / 12) + (WIDTH / 6) * (i % 6), (HEIGHT / 5) * ((i // 6) + 1), function)

        self.waiting = True
        while self.waiting and self.running:
            self.ui.update()
            self.events()

            self.screen.fill(GREY)
            self.ui.draw(self.screen)

            for i in range(len(self.map.maps)):
                if self.unlockedLevel >= i:
                    info = ""
                else:
                    info = " (Locked)"
                self.drawText("Level " + str(i + 1) + info, 20, WHITE,
                              (WIDTH / 12) + (WIDTH / 6) * (i % 6), (HEIGHT / 5) * ((i // 6) + 1) + 40)
            pg.display.flip()

    def nextLevel(self):
        # to be called up by a button press
        self.waiting = False

    def drawText(self, text, size, color, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        self.screen.blit(textSurface, textRect)

    def showWinScreen(self):
        # delete remaing ui
        for ui in self.ui:
            ui.kill()
        for sprite in self.allSprites:
            sprite.kill()

        # make the background image
        for row, tiles in enumerate(self.map.background):
            for col, tile in enumerate(tiles):
                if tile.isnumeric():
                    Platform(self, col, row, tile)

        # make buttons
        if self.curLvl + 1 < len(self.map.maps):
            Button(self, WIDTH / 2, HEIGHT * 2 / 3, self.nextLevel)
        Button(self, WIDTH / 2, HEIGHT * 5 / 6, self.showMenuScreen)

        pg.display.flip()

        self.waiting = True
        while self.waiting and self.running:
            # waiting is set to false through button
            self.clock.tick(FPS)

            # update
            self.update()
            self.ui.update()
            self.events()

            # draw
            self.screen.fill(GREY)
            self.allSprites.draw(self.screen)
            self.ui.draw(self.screen)

            # draw text
            self.drawText("Level Complete!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.drawText("Ghosts: " + str(self.player.lifeNum), 32, WHITE, WIDTH / 2, HEIGHT / 2)
            if self.curLvl + 1 < len(self.map.maps):
                self.drawText("Next level", 35, BLACK, WIDTH / 2, HEIGHT * 2 / 3 - 20)
            self.drawText("Level select", 35, BLACK, WIDTH / 2, HEIGHT * 5 / 6 - 20)

            # display
            pg.display.flip()
