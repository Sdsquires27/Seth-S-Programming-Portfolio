# Chucklehead
# Seth Squires
# 3/22 - 4/22

import random

import pygame

from player import *
import cardGraphics as cg
import chuckleClasses as ch

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chucklehead")

clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
cardImages = {}
cardImages["Back"] = pygame.image.load(os.path.join(imgFolder, "playing card.jfif"))
cardImages["Hearts"] = []

testCard = cg.Card(cardImages, WIDTH/2, HEIGHT/2)
allSprites.add(testCard)

# set up game

# create deck
deck = ch.ChuckleDeck

# create players
playerList = []
# default is four, change this later
players = 4
for i in range(players):
    x = ch.Player(str.format("Player {}", i))
    playerList.append(x)

# create card graphics

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            testCard.click()

    # Update
    allSprites.update()

    # Draw / render
    screen.fill(BLACK)
    allSprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
