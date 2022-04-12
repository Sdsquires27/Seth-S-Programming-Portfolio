# Chucklehead
# Seth Squires
# 3/22 - 4/22

import random

import pygame

from player import *
import cardGraphics as cg
import chuckleClasses as ch
import ui

# initialize pygame and create window
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Chucklehead")

clock = pygame.time.Clock()

allSprites = pygame.sprite.Group()
cards = pygame.sprite.Group()
selectedCard = pygame.sprite.Group()
topDeck = pygame.sprite.Group()

cardImages = {}

# initialize the background image
background = pygame.image.load(os.path.join(imgFolder, "card table.png"))
background_rect = background.get_rect()

# initialize the playable space image
playSpot = pygame.image.load(os.path.join(cardFolder, "Play Here.jfif"))
buttonImage = pygame.image.load(os.path.join(imgFolder, "button.png"))

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

# make play spot
playSpot = cg.playSpot(playSpot, WIDTH / 2 - 100, HEIGHT / 6, topDeck)
allSprites.add(playSpot)

# make holding hand
cardHold = cg.HeldCards("Hold")

# make take deck button
takeDiscard = ui.PgButton(buttonImage, playSpot)
allSprites.add(takeDiscard)

# create deck
deck = cg.Deck(cardImages, playSpot, selectedCard, cardHold)
deck.createDeck()
deck.shuffle()

# make cards appear
for card in deck.cards:
    allSprites.add(card)
    cards.add(card)

# create players
playerList = []
downDecks = []
upDecks = []
hands = []
# default is four, change this later
players = 4
for i in range(players):
    # Name is set simply to the player number. change this later.
    x = cg.Player(str.format("Player {}", i+1), (i + 1) * 400 - 300, HEIGHT - 300, 0)

    # add the player's three different decks to a list of the decks.
    downDecks.append(x.downCards)
    upDecks.append(x.upCards)
    hands.append(x.hand)

    playerList.append(x)

playSpot.setPlayers(playerList)

deck.deal(downDecks, 3)
deck.deal(upDecks, 3)
deck.deal(hands, 3)

curTurn = 0
takeDiscard.setPlayer(playerList[curTurn])

def newTurn():
    playerList[curTurn].curTurn = True


# Game loop
running = True
newTurn()
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cardHold.click(cards)
            for card in cards:
                card.click()
            takeDiscard.click()
    # Update
    # if the turn has moved on
    if playSpot.curTurn != curTurn:
        playerList[curTurn].curTurn = False
        if deck.cards and playerList[curTurn].hand.cards and playerList[curTurn].hand.handLength < 3:
            deck.giveCard(deck.cards[0], playerList[curTurn].hand)

        curTurn = playSpot.curTurn
        playerList[curTurn].curTurn = True
        takeDiscard.setPlayer(playerList[curTurn])

    allSprites.update()
    for player in playerList:
        player.update()
    deck.update()

    cardHold.update()


    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    allSprites.draw(screen)
    topDeck.draw(screen)
    selectedCard.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
