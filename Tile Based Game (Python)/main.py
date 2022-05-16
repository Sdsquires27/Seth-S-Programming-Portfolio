# Pygame template - skeleton for a new pygame project
import pygame as pg
import random
from os import path
from player import *
from wall import *
from tilemap import *
from mobs import *
from item import *

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
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        pg.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.loadData()
        pg.key.set_repeat(500, 100)

    def loadData(self):

        self.hudFont = path.join(imgFolder, "Impacted2.0.ttf")
        self.titleFont = path.join(imgFolder, "ZOMBIE.TTF")
        self.dimScreen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dimScreen.fill((0, 0, 0, 180))

        self.playerImg = pg.image.load(os.path.join(imgFolder, "manBlue_silencer.png")).convert()
        self.mobImg = pg.image.load(os.path.join(imgFolder, MOB_IMAGE)).convert()
        self.bulletImages = {}
        self.bulletImages["lg"] = pg.image.load(os.path.join(imgFolder, BULLET_IMG)).convert()
        self.bulletImages["sm"] = pg.transform.scale(self.bulletImages["lg"], (10, 10))

        self.splat = pg.image.load(path.join(imgFolder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))

        self.gunFlashes = []
        for img in MUZZLE_FLASHES:
            self.gunFlashes.append(pg.image.load(path.join(imgFolder, img)).convert_alpha())

        self.itemImages = {}
        for item in ITEM_IMAGES:
            self.itemImages[item] = pg.image.load(path.join(imgFolder, ITEM_IMAGES[item])).convert_alpha()

        self.wallImg = pg.image.load(os.path.join(imgFolder, WALL_IMG)).convert()
        self.wallImg = pg.transform.scale(self.wallImg, (TILESIZE, TILESIZE))

        # sounds
        pg.mixer.music.load(path.join(sndFolder, BG_MUSIC))
        self.effectSounds = {}
        for type in EFFECTS_SOUNDS:
            self.effectSounds[type] = pg.mixer.Sound(path.join(sndFolder, EFFECTS_SOUNDS[type]))
        self.weaponSounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weaponSounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(sndFolder, snd))
                s.set_volume(0.1)
                self.weaponSounds[weapon].append(s)
        self.zombieMoanSounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(sndFolder, snd))
            s.set_volume(0.2)
            self.zombieMoanSounds.append(s)
        self.playerHitSounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(sndFolder, snd))
            s.set_volume(0.5)
            self.playerHitSounds.append(s)
        self.zombieHitSounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(sndFolder, snd))
            s.set_volume(0.3)
            self.zombieHitSounds.append(s)

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

        self.allSprites = pygame.sprite.LayeredUpdates()
        self.mobs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.map = TiledMap(path.join(mapFolder, "level1.tmx"))
        self.mapImg = self.map.makeMap()
        self.mapRect = self.mapImg.get_rect()

        for tileObject in self.map.tmxdata.objects:
            objCenter = vec(tileObject.x + tileObject.width / 2, tileObject.y + tileObject.height / 2)
            if tileObject.name == "player":
                self.player = Player(self, objCenter.x, objCenter.y)
                self.allSprites.add(self.player)
            if tileObject.name == "wall":
                Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
            if tileObject.name == "zombie":
                 Mob(self, objCenter.x, objCenter.y)
            if tileObject.name in ["health", "shotgun"]:
                Item(self, objCenter, tileObject.name)


        self.camera = Camera(self.map.width, self.map.height)
        self.drawDebug = False
        self.paused = False
        self.effectSounds["level_start"].play()

        g.run()

    def run(self):
        # Game loop
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()


    def quit(self):
        pg.quit()

    def drawText(self, text, fontname, size, color, x, y):
        font = pygame.font.Font(fontname, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midbottom = (x, y)
        self.screen.blit(textSurface, textRect)

    def update(self):
        # Game Loop - Update
        self.allSprites.update()
        self.camera.update(self.player)

        if len(self.mobs) < 1:
            self.playing = False

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collideHitRecT)
        for hit in hits:
            if random.random() < 0.7:
                choice(self.playerHitSounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effectSounds["health_up"].play()
                self.player.addHealth(HEALTH_PACK_AMOUNT)
            elif hit.type == "shotgun":
                hit.kill()
                self.effectSounds["gunPickup"].play()
                self.player.weapon = "shotgun"

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            # hit.health -= WEAPONS[self.player.weapon]["damage"] * len(hits[hit])
            for b in hits[hit]:
                hit.health -= b.damage
            hit.vel = vec(0, 0)

    def events(self):
        # Game loop - Event
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_h:
                    self.drawDebug = not self.drawDebug
                if event.key == pg.K_p:
                    self.paused = not self.paused

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
        self.drawText("Zombies: {}".format(len(self.mobs)), self.hudFont, 30, WHITE, WIDTH - 80, 10)

        # *after* drawing everything, flip the display
        if self.paused:
            self.screen.blit(self.dimScreen, (0, 0))
            self.drawText("Paused", self.titleFont, 105, RED, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()

    def showStartScreen(self):
        # game splash/start screen
        pass

    def showGoScreen(self):
        # game over screen
        self.screen.fill(BLACK)
        self.drawText("GAME OVER", self.titleFont, 100, RED, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press a key to start", self.titleFont, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.waitForKeys()

    def waitForKeys(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()
g.showStartScreen()
while g.running:
    g.new()
    g.showGoScreen()

pygame.quit()
