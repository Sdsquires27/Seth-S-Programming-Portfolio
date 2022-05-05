from player import *
from platform import *
from levelData import *
from button import *
from spritesheet import *


class Game:
    def __init__(self):
        # initialize pygame and create window
        self.playerImg = None
        self.buttonImages = None

        self.running = True
        self.waiting = False
        self.playing = False

        self.curX = 0
        self.curY = 0
        self.curLev = 0
        self.fontName = pg.font.match_font(FONT_NAME)
        self.unlockedLevel = 0

        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game")
        self.clock = pg.time.Clock()
        self.loadData()
        self.player = None

    def loadData(self):
        self.dir = os.path.dirname(__file__)

        self.playerSpritesheet = Spritesheet(os.path.join(imgFolder, PLAYER_SPRITESHEET))
        self.enemySpritesheet = Spritesheet(os.path.join(imgFolder, ENEMY_SPRITESHEET))

        self.buttonImages = []
        self.buttonImages.append(pg.image.load(os.path.join(imgFolder, "button1.jpg")).convert())
        self.buttonImages.append(pg.image.load(os.path.join(imgFolder, "button2.jpg")).convert())

        with open(os.path.join(self.dir, LEVEL_FILE), "r") as f:
            try:
                self.unlockedLevel = int(f.read())
            except:
                self.unlockedLevel = 0

    def new(self):
        # initialize the game
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # initialize player
        self.player = Player(self)
        self.allSprites.add(self.player)

        # load level
        self.showMenuScreen()
        for plat in LEVELS[self.curLev]:
            Platform(*plat, self)

        self.curX = 0
        self.curY = 0

        self.run()

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

        # test function, unused.
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
                self.curLev += 1

                # if you have reached a new highest level, increase unlocked levels
                if self.curLev > self.unlockedLevel:
                    print("new level unlocked")
                    self.unlockedLevel = self.curLev
                    with open(os.path.join(self.dir, LEVEL_FILE), "w") as f:
                        f.write(str(self.unlockedLevel))

                self.showWinScreen()
                if self.running:
                    self.newLevel()

    def newLevel(self):
        # for calling up new level

        # delete all sprites
        for sprite in self.allSprites:
            sprite.kill()

        # load level
        for plat in LEVELS[self.curLev]:
            Platform(*plat, self)

        # reset player
        self.player = Player(self)
        self.allSprites.add(self.player)

        self.curX = 0
        self.curY = 0

        self.run()

    def moveScreen(self):
        # NOTE: This script is not finished. This was a test for scrolling platforms.

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
                if self.waiting:
                    self.waiting = False
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

    def nextLevel(self):
        # to be called up by a button press
        self.waiting = False

    def showStartScreen(self):
        # game splash/start screen
        self.screen.fill(BLUE)
        self.drawText("Wow, you died a lot", 60, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Arrow keys to move, space to jump. Press twice to double jump", 40, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press any key to start", 40, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
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

    def showMenuScreen(self):
        # delete any buttons that might already exist
        for ui in self.ui:
            ui.kill()

        for i in range(len(LEVELS)):
            if self.unlockedLevel >= i:
                function = lambda i2=i: self.exitMenuScreen(i2)
            else:
                function = None
            Button(self, (WIDTH / 12) + (WIDTH / 6) * (i % 6), (HEIGHT / 5) * ((i // 6) + 1), function)

        self.waiting = True
        while self.waiting:
            self.ui.update()
            self.events()

            self.screen.fill(BLUE)
            self.ui.draw(self.screen)

            for i in range(len(LEVELS)):
                if self.unlockedLevel >= i:
                    info = ""
                else:
                    info = " (Locked)"
                self.drawText("Level " + str(i + 1) + info, 20, WHITE,
                              (WIDTH / 12) + (WIDTH / 6) * (i % 6), (HEIGHT / 5) * ((i // 6) + 1) + 40)
            pg.display.flip()

    def exitMenuScreen(self, level):
        # pass into button
        self.waiting = False
        self.curLev = level
        for ui in self.ui:
            ui.kill()

    def showWinScreen(self):
        # delete remaing ui
        for ui in self.ui:
            ui.kill()

        # make buttons
        Button(self, WIDTH / 4, HEIGHT * 2 / 3, self.nextLevel)
        Button(self, WIDTH * 3 / 4, HEIGHT * 2 / 3, self.showMenuScreen)

        pg.display.flip()

        self.waiting = True
        while self.waiting:
            # waiting is set to false through button
            if not self.ghosts:
                self.player.win()
            self.clock.tick(FPS)

            # update
            self.update()
            self.ui.update()
            self.events()

            # draw
            self.screen.fill(BLUE)
            self.allSprites.draw(self.screen)
            self.ui.draw(self.screen)

            # draw text
            self.drawText("Level Complete!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.drawText("Deaths: " + str(self.player.lifeNum), 32, WHITE, WIDTH / 2, HEIGHT / 2)
            self.drawText("Next level", 40, BLACK, WIDTH / 4, HEIGHT * 2 / 3 - 10)
            self.drawText("Level select", 40, BLACK, WIDTH * 3 / 4, HEIGHT * 2 / 3 - 10)

            # display
            pg.display.flip()
