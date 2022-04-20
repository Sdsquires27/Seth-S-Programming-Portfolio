# Chucklehead
# Seth Squires
# 3/22 - 4/22


import pygame

from player import *
import cardGraphics as cg
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
darkButtonImage = pygame.image.load(os.path.join(imgFolder, "darkButton.png"))

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

# initialize game sounds
shuffleSound = pygame.mixer.Sound(os.path.join(sndFolder, "shuffle.wav"))

pygame.mixer.music.load(os.path.join(sndFolder, "mainTheme.ogg"))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops=-1)


cardSounds = {}
cardSounds["Pickup"] = []
cardSounds["Place Down"] = []
for i in range(3):
    cardSounds["Pickup"].append(pygame.mixer.Sound(os.path.join(sndFolder, str.format("cardSlide{}.wav", i+1))))
    cardSounds["Place Down"].append(pygame.mixer.Sound(os.path.join(sndFolder, str.format("cardPlace{}.wav", i+1))))

# set up game

# make play spot
playSpot = cg.playSpot(playSpot, WIDTH / 2 - 100, HEIGHT / 6, topDeck)
allSprites.add(playSpot)

# make holding hand
cardHold = cg.HeldCards("Hold")

# make take deck button
takeDiscard = ui.PgButton(buttonImage, darkButtonImage, playSpot)
allSprites.add(takeDiscard)

# create deck
deck = cg.Deck(cardImages, playSpot, selectedCard, cardHold, cardSounds)
deck.createDeck()
deck.shuffle()

# make cards appear
for card in deck.cards:
    allSprites.add(card)
    cards.add(card)

# create players (rest of the provess is in the new game)
playerList = []
downDecks = []
upDecks = []
hands = []
curTurn = 0


def drawText(surf, text, size, x, y, color):
    font = pygame.font.Font(fontArial, size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    surf.blit(textSurface, textRect)


def showStartScreen():
    screen.blit(background, background_rect)
    drawText(screen, "Chucklehead", 65, WIDTH / 2, HEIGHT / 4, WHITE)
    i = 0
    for rule in chuckleRules:
        i += 1
        drawText(screen, rule, 18, WIDTH / 2, HEIGHT / 3 + i * 20, WHITE)
    drawText(screen, "Click a number from two to four to determine the number of players.",
             36, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 3
                elif event.key == pygame.K_4:
                    return 4


def newTurn():
    playerList[curTurn].curTurn = True

def newGame():
    # player number is equal to key pressed
    players = showStartScreen()
    shuffleSound.play()
    pygame.mixer.music.set_volume(.75)
    for i in range(players):
        # Name is set simply to the player number. change this later.
        x = cg.Player(str.format("Player {}", i + 1), (i + 1) * 400 - 300, HEIGHT - 300, cardHold)

        # add the player's three different decks to a list of the decks.
        downDecks.append(x.downCards)
        upDecks.append(x.upCards)
        hands.append(x.hand)

        playerList.append(x)

    # tell the play spot who the players are for turn purposes
    playSpot.setPlayers(playerList)

    # deal cards
    deck.deal(downDecks, 3)
    deck.deal(upDecks, 3)
    deck.deal(hands, 3)

    takeDiscard.setPlayer(playerList[curTurn])

def nextTurn(playerName):
    # pause between turns so that people don't cheat and stuff
    screen.blit(background, background_rect)
    drawText(screen, playerName+"'s turn!", 65, WIDTH / 2, HEIGHT / 4, WHITE)
    drawText(screen, "Press any key to play.", 36, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def showWinScreen(winner):
    # tell the player who wins (:
    pygame.mixer.music.set_volume(1)
    screen.blit(background, background_rect)
    drawText(screen, winner+" wins!", 65, WIDTH / 2, HEIGHT / 4, WHITE)
    drawText(screen, "Press any key to return to the tile screen.", 18, WIDTH / 2, HEIGHT * 3 / 4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Game loop
running = True
newGame()
newTurn()
nextTurn(playerList[curTurn].name)
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

        # if the deck and player has cards and the player has less than three cards
        if deck.cards and playerList[curTurn].hand.cards and playerList[curTurn].hand.handLength < 3:
            deck.giveCard(deck.cards[0], playerList[curTurn].hand)

        curTurn = playSpot.curTurn
        playerList[curTurn].curTurn = True
        takeDiscard.setPlayer(playerList[curTurn])
        nextTurn(playerList[curTurn].name)
    # check for winner
    for play in playerList:
        if not play.hand.cards and not play.upCards.cards and not play.downCards.cards and not cardHold.cards:
            showWinScreen(play.name)
            newGame()
            newTurn()



    # update sprites
    allSprites.update()

    # update players
    for player in playerList:
        player.update()

    # update deck
    deck.update()

    # update hand holding cards
    cardHold.update()


    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)

    # draw all sprites
    allSprites.draw(screen)

    # draw the top card of the deck
    topDeck.draw(screen)

    # draw the card in your hand
    selectedCard.draw(screen)

    # draw text
    drawText(screen, "Take pile", 36, WIDTH - 200, HEIGHT / 5 + 20, WHITE)
    for player in playerList:
        addY = 100
        if len(player.hand.cards) > 3:
            addY = 230
        drawText(screen, player.name, 18, player.x + 110, player.y + addY, WHITE)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
