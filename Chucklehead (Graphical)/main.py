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
cards = pygame.sprite.Group()

cardImages = {}
# initialize the deck images
cardImages["Back"] = pygame.image.load(os.path.join(cardFolder, "Back.jfif"))
cardImages["Hearts"] = []
cardImages["Spades"] = []
cardImages["Clubs"] = []
cardImages["Diamonds"] = []

# Add each card into its own group.
for i in range(13):
    cardImages["Hearts"].append(pygame.image.load(os.path.join(cardFolder, str.format("Hearts {}.png", i + 1))))
for i in range(13):
    cardImages["Spades"].append(pygame.image.load(os.path.join(cardFolder, str.format("Spades {}.png", i + 1))))
for i in range(13):
    cardImages["Clubs"].append(pygame.image.load(os.path.join(cardFolder, str.format("Club {}.png", i + 1))))
for i in range(13):
    cardImages["Diamonds"].append(pygame.image.load(os.path.join(cardFolder, str.format("Diamond {}.png", i + 1))))




# set up game

# create deck
deck = cg.Deck(cardImages)
deck.createDeck()

# make cards appear
for card in deck.cards:
    allSprites.add(card)
    cards.add(card)
deck.cards[len(deck.cards) - 1].selectable = True

# create players
playerList = []
downDecks = []
upDecks = []
hands = []
# default is four, change this later
players = 4
for i in range(players):
    # Name is set simply to the player number. change this later.
    x = cg.Player(str.format("Player {}", i+1), 0, 0)
    downDecks.append(x.downCards)
    upDecks.append(x.upCards)
    hands.append(x.hand)
    playerList.append(x)

deck.deal(downDecks, 3)
deck.deal(upDecks, 3)
deck.deal(hands, 3)




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
            for card in cards:
                card.click()

    # Update
    allSprites.update()

    # Draw / render
    screen.fill(BLACK)
    allSprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
