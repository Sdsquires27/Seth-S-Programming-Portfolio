import pygame
import hands as h
import chuckleClasses as ch
from settings import *

class GraphicalHand(ch.ChuckleHand):
    def __init__(self, type):
        super(GraphicalHand, self).__init__()
        self.type = type


    def giveCard(self, card, other_hand):
        self.cards.remove(card)
        card.owner = other_hand
        other_hand.addCard(card)


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
        self.multiCards = []

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
            if self.multiCards:
                for card in self.multiCards:
                    card.defaultPos = (self.x, self.y)
                    self.rect.right += 75

        else:
            self.rect.center = self.defaultPos

    def click(self, cards):
        if self.selectable:

            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                if not self.selected:
                    otherSelected = False
                    for card in cards:
                        if card.selected:
                            otherSelected = True

                    if not otherSelected:
                        self.selectedCard.add(self)
                        self.selected = True

                else:
                    # unselect if not touching another card of same value, check if played
                    
                    self.selected = False
                    self.selectedCard.remove(self)


                    for card in cards:
                        if card != self:
                            if self.rect.colliderect(card.rect):
                                print("Card collision")
                                if card.value == self.value and card.owner == self.owner:
                                    print("Card is same value and same owner")
                                    if card.owner.  type == "Hand":
                                        print("Card's owner is hand")
                                        if not card.selected:
                                            print("Card grabbed")
                                            self.selectedCard.add(self)
                                            self.selectedCard.add(card)
                                            self.selected = True

                                            self.multiCards.append(card)


                    if self.rect.colliderect(self.playRect):
                        self.selected = False
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
            card.x = WIDTH/2 + 100 + i
            card.y = HEIGHT/6
            card.faceUp = False

    def giveCard(self, card, other_hand):
        self.cards.remove(card)
        card.owner = other_hand
        other_hand.addCard(card)

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
        self.upCards = GraphicalHand("Up")
        self.downCards = GraphicalHand("Down")
        self.hand = GraphicalHand("Hand")
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
                card.show()
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
        self.curTurn = 0
        self.turnOver = False



    def tryPlayCard(self, card):

        self.turnOver = False
        # if no cards, play card
        if not self.discard.cards:
            self.playCard(card)

        # if cards, check that card is higher or equal than previous card (or lower if seven)
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

        # if top card is a ten, clear pile
        if self.discard.cards:
            if self.discard.cards[len(self.discard.cards) - 1].value == 9:
                self.clearCards()

        # next turn
        if self.turnOver:
            self.curTurn += 1
            if self.curTurn > 3:
                self.curTurn = 0



    def clearCards(self):
        for card in self.discard.cards:
            card.kill()

        self.discard.cards.clear()


    def playCard(self, card):
        card.x = self.x
        card.y = self.y
        card.owner.giveCard(card, self.discard)
        card.selectable = False
        self.topDeck.empty()
        self.topDeck.add(card)
        self.turnOver = True
