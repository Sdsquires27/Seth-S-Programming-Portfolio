# Pygame template - skeleton for a new pygame project
import pygame as pg
import random
from os import path
from player import *
from wall import *
from tilemap import *
from mobs import *

# HUD functions
def drawPlayerHealth(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outlineRect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fillRect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fillRect)
    pg.draw.rect(surf, WHITE, outlineRect, 2)

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
        self.mobs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.map = TiledMap(path.join(mapFolder, "level1.tmx"))
        self.mapImg = self.map.makeMap()
        self.mapRect = self.mapImg.get_rect()

        self.playerImg = pg.image.load(os.path.join(imgFolder, "manBlue_silencer.png")).convert()
        self.mobImg = pg.image.load(os.path.join(imgFolder, MOB_IMAGE)).convert()
        self.bulletImg = pg.image.load(os.path.join(imgFolder, BULLET_IMG)).convert()

        self.wallImg = pg.image.load(os.path.join(imgFolder, WALL_IMG)).convert()
        self.wallImg = pg.transform.scale(self.wallImg, (TILESIZE, TILESIZE))

    def new(self):
        # initialize the game

        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self, col, row)
        #         if tile == "M":
        #             Mob(self, col, row)
        #         if tile == "P":
        #             self.player = Player(self, col, row)
        #             self.allSprites.add(self.player)

        for tileObject in self.map.tmxdata.objects:
            if tileObject.name == "player":
                self.player = Player(self, tileObject.x, tileObject.y)
                self.allSprites.add(self.player)
            if tileObject.name == "wall":
                Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
            if tileObject.name == "zombie":
                 Mob(self, tileObject.x, tileObject.y)

        self.camera = Camera(self.map.width, self.map.height)
        self.drawDebug = False

        g.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.allSprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collideHitRecT)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DMG
            hit.vel = vec(0, 0)

    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.drawDebug = not self.drawDebug

    def drawGrid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, GREEN, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, GREEN, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # game loop - draw
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.mapImg, self.camera.applyRect(self.mapRect))
        for sprite in self.allSprites:
            if isinstance(sprite, Mob):
                sprite.drawHealth()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.drawDebug:
                pg.draw.rect(self.screen, WHITE, self.camera.applyRect(sprite.hitRect), 1)

        if self.drawDebug:
            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.applyRect(wall.rect), 1)

        # self.drawGrid()
        # HUD functions
        drawPlayerHealth(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def showStartScreen(self):
        # game splash/start screen
        pass

    def showGoScreen(self):
        # game over screen
        self.running = False

g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGoScreen()

pygame.quit()
