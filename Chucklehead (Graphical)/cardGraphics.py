import pygame
import hands as h
import chuckleClasses as ch
from settings import *

class Card(pygame.sprite.Sprite):

    RANK = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    SUIT = ["Hearts", "Diamonds", "Spades", "Clubs"]

    def __init__(self, sprites, x, y, rank, suit, playSpot, owner, selectedCard):
        super(Card, self).__init__()
        self.selectable = False
        self.back = pygame.transform.scale(sprites["Back"], (100, 150))
        self.front = pygame.transform.scale(sprites[suit][rank], (100, 150))

        self.owner = owner

        self.selectedCard = selectedCard

        self.value = rank
        if self.value == 0:
            self.value = 13

        self.image = self.front
        self.rect = self.image.get_rect()
        self.selected = False
        self.faceUp = True
        self.x = x
        self.y = y
        self.playSpot = playSpot
        self.playRect = playSpot.rect
        self.defaultPos = (self.x, self.y)

    def hide(self):
        self.faceUp = False

    def show(self):
        self.faceUp = True

    def update(self):
        if self.faceUp:
            self.image = self.front
        else:
            self.image = self.back


        self.defaultPos = (self.x, self.y)
        if self.selected:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.center = self.defaultPos

    def click(self):
        if self.selectable:

            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                if not self.selected:
                    self.selectedCard.add(self)
                    self.selected = True
                else:

                    # unselect, check if played
                    self.selected = False
                    if self.rect.colliderect(self.playRect):
                        self.selectedCard.remove(self)
                        self.playSpot.tryPlayCard(self)


class Deck(h.Deck):
    def __init__(self, sprites, playSpot, selectedCard):
        super(Deck, self).__init__()
        self.sprites = sprites
        self.playSpot = playSpot
        self.selectedCard = selectedCard

    def update(self):
        for i in range(len(self.cards)):
            card = self.cards[i]
            card.x = WIDTH/2 + i
            card.y = HEIGHT/3
            card.faceUp = False

    def deal(self, hands_list, perHand=1):
        for i in range(perHand):
            for hand in hands_list:
                topCard = self.cards[0]
                topCard.owner = hand
                self.giveCard(topCard, hand)



    def createDeck(self):
        for suit in Card.SUIT:
            for rank in Card.RANK:
                card = Card(self.sprites, 0, 0, rank, suit, self.playSpot, self, self.selectedCard)
                self.addCard(card)

class Player(ch.Player):
    def __init__(self, name, x, y, rot):
        super(Player, self).__init__(name)
        self.x = x
        self.y = y
        self.rot = rot
        self.curTurn = False

    def update(self):


        for i in range(len(self.hand.cards)):
            card = self.hand.cards[i]
            card.x = self.x + i * 100 + 10
            card.y = self.y
            if not self.curTurn:
                card.hide()
                card.selectable = False
            else:
                card.selectable = True


        for i in range(len(self.downCards.cards)):
            card = self.downCards.cards[i]
            card.x = self.x + i * 110
            card.y = self.y - 110
            card.hide()

            if self.curTurn:
                if not self.hand.cards and not self.upCards.cards:
                    card.selectable = True

        for i in range(len(self.upCards.cards)):
            card = self.upCards.cards[i]
            card.x = self.x + i * 110
            card.y = self.y - 110

            if self.curTurn:
                if not self.hand.cards:
                    card.selectable = True

class playSpot(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, topDeckGroup):
        super(playSpot, self).__init__()
        self.x = x
        self.y = y
        self.topDeck = topDeckGroup
        self.image = pygame.transform.scale(sprite, (100, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.discard = ch.ChuckleHand()



    def tryPlayCard(self, card):

        # if no cards, play card
        if not self.discard.cards:
            self.playCard(card)

        # if card, check that card is higher or equal than previous card (or lower if seven)
        else:
            topCard = self.discard.cards[len(self.discard.cards) - 1]

            # if card is not a seven
            if topCard.value != 6:
                # if card is greater than, equal to, or a 2
                if card.value >= topCard.value or card.value == 1:
                    self.playCard(card)

            elif topCard.value == 6:
                if card.value <= topCard.value:
                    self.playCard(card)


        # Check for special effects

        # if top four cards are the same
        if len(self.discard.cards) >= 4:
            topCards = []
            for i in range(4):
                topCards.append(self.discard.cards[len(self.discard.cards) - (i + 1)].value)
            if topCards[0] == topCards[1] == topCards[2] == topCards[3]:
                self.clearCards()


        # if top card is a ten
        if card.value == 9:
            print("Destroy cards")
            self.clearCards()

        # next turn


    def clearCards(self):
        for card in self.discard.cards:
            card.kill()


    def playCard(self, card):
        card.x = self.x
        card.y = self.y
        card.owner.giveCard(card, self.discard)
        card.selectable = False
        self.topDeck.empty()
        self.topDeck.add(card)
