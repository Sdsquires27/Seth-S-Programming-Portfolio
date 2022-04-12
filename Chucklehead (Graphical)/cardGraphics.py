import pygame
import hands as h
import chuckleClasses as ch
from settings import *


class GraphicalHand(ch.ChuckleHand):
    def __init__(self, handType):
        super(GraphicalHand, self).__init__()
        self.type = handType


    def giveCard(self, card, other_hand):
        self.cards.remove(card)
        card.owner = other_hand
        other_hand.addCard(card)
        if other_hand.type == "Hand" or other_hand.type == "Down" or other_hand.type == "Up":
            card.defaultOwner = other_hand

    @property
    def handLength(self):
        return len(self.cards)



class HeldCards(GraphicalHand):

    def update(self):
        if self.cards:
            for i in range(len(self.cards)):
                card = self.cards[i]
                x, y = pygame.mouse.get_pos()
                card.x = x
                card.y = y
                card.x += 50 * i

    def click(self, cards):
        noCollisions = True
        if self.cards:
            for card in self.cards:
                if card.collisionTest(cards) != "No collisions":
                    noCollisions = False
                    break
            if noCollisions:
                self.returnCards()


    def tryPlayCards(self):
        if self.cards:
            self.cards[0].playSpot.tryPlayCard(self.cards)

    def returnCards(self):
        for card in self.cards:
            card = self.cards[0]
            self.giveCard(card, card.defaultOwner)
            card.selectedCard.remove(card)
            card.selectable = False



class Card(pygame.sprite.Sprite):

    RANK = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    SUIT = ["Hearts", "Diamonds", "Spades", "Clubs"]

    def __init__(self, sprites, x, y, rank, suit, playSpot, owner, selectedCard, cardHolder):
        super(Card, self).__init__()
        self.selectable = False
        self.back = pygame.transform.scale(sprites["Back"], (100, 150))
        self.front = pygame.transform.scale(sprites[suit][rank], (100, 150))

        self.owner = owner
        self.defaultOwner = self.owner

        self.cardHolder = cardHolder

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
        self.rect.center = self.defaultPos

    def click(self):
        if self.selectable:

            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                if not self.selected:
                    self.selectedCard.add(self)
                    self.selected = True
                    self.owner.giveCard(self, self.cardHolder)

                    # unselect if not touching another card of same value, check if played
                    # cardSelected = False
                    # selectedCard = None
                    # for card in cards:
                    #     if card != self:
                    #         if self.rect.colliderect(card.rect):
                    #             if card.value == self.value and card.owner == self.defaultOwner:
                    #                 if card.owner.type == "Hand":
                    #                     if not card.selected:
                    #                         print("card grabbed")
                    #                         print(card.owner.type)
                    #                         cardSelected = True
                    #                         selectedCard = card
                    #
                    #
                    #
                    # if self.rect.colliderect(self.playRect):
                    #     self.selected = False
                    #     self.playSpot.tryPlayCard(self)
                    # else:
                    #     if cardSelected:
                    #         selectedCard.selected = True
                    #         selectedCard.owner.giveCard(selectedCard, self.cardHolder)
                    #         selectedCard.selected = True
                    #         self.selectedCard.add(selectedCard)
                    #
                    #     else:
                    #         self.selected = False
                    #         self.owner.giveCard(self, self.defaultOwner)
                    #         self.selectedCard.remove(self)

        else:
            if self.selected:
                self.selectable = True
                self.selected = False




    def selectedClick(self, cards):
        cardSelected = False




    def collisionTest(self, cards):
        cardSelected = False
        for card in cards:
                if not card.selected and \
                self.rect.colliderect(card.rect) and \
                card.value == self.value and card.owner == self.defaultOwner and \
                card.owner.type == "Hand":
                    card.selected = True
                    card.owner.giveCard(card, self.cardHolder)
                    cardSelected = True
                    self.selectedCard.add(card)
        if cardSelected:
            return "Card picked"

        if self.rect.colliderect(self.playRect):
            self.cardHolder.tryPlayCards()
            return "Play Cards"
        elif not cardSelected:
            return "No collisions"

        return None

class Deck(h.Deck):
    def __init__(self, sprites, playSpot, selectedCard, cardHolder):
        super(Deck, self).__init__()
        self.sprites = sprites
        self.playSpot = playSpot
        self.selectedCard = selectedCard
        self.cardHolder = cardHolder

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
        if other_hand.type == "Hand" or other_hand.type == "Down" or other_hand.type == "Up":
            card.defaultOwner = other_hand

    def deal(self, hands_list, perHand=1):
        for i in range(perHand):
            for hand in hands_list:
                topCard = self.cards[0]
                topCard.owner = hand
                self.giveCard(topCard, hand)



    def createDeck(self):
        for suit in Card.SUIT:
            for rank in Card.RANK:
                card = Card(self.sprites, 0, 0, rank, suit, self.playSpot, self, self.selectedCard, self.cardHolder)
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
            card.x = self.x + (i % 3) * 100 + 10
            card.y = self.y + ((i // 3) * 150)
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
        self.discard = GraphicalHand("Discard")
        self.curTurn = 0
        self.turnOver = False
        self.players = None

    def setPlayers(self, playerList):
        self.players = playerList

    def tryPlayCard(self, cards):
        curPlayer = self.players[self.curTurn]
        self.turnOver = False
        # if no cards, play card
        if not self.discard.cards:
            self.playCard(cards)

        # if cards, check that card is higher or equal than previous card (or lower if seven)
        else:
            topCard = self.discard.cards[len(self.discard.cards) - 1]
            card = cards[0]
            # if card is not a seven
            if topCard.value != 6:
                # if card is greater than, equal to, or a 2
                if card.value >= topCard.value or card.value == 1:
                    self.playCard(cards)
                else:
                    if card.faceUp:
                        card.cardHolder.returnCards()
                    else:
                        self.giveToHand(curPlayer.hand)
                        self.turnOver = True

            elif topCard.value == 6:
                if card.value <= topCard.value:
                    self.playCard(cards)
                else:
                    if card.faceUp:
                        card.cardHolder.returnCards()
                    else:
                        self.giveToHand(curPlayer.hand)
                        self.turnOver = True

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

    def giveToHand(self, otherHand):
        max = False
        for i in range(len(self.discard.cards)):
            if not max:
                if len(otherHand.cards) > 5:
                    max = True
                else:
                    topCard = self.discard.cards[len(self.discard.cards) - 1]
                    self.discard.giveCard(topCard, otherHand)
            else:
                self.clearCards()
        self.curTurn += 1
        if self.curTurn > 3:
            self.curTurn = 0

    def clearCards(self):
        for card in self.discard.cards:
            card.kill()

        self.discard.cards.clear()

    def playCard(self, cards):
        for i in range(len(cards)):
            card = cards[0]
            card.x = self.x
            card.y = self.y
            card.owner.giveCard(card, self.discard)
            card.selectable = False
            card.selected = False
            if not card.faceUp:
                card.show()
        self.topDeck.empty()
        self.topDeck.add(self.discard.cards[len(self.discard.cards) - 1])
        self.turnOver = True
