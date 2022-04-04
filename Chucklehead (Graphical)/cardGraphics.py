import pygame
import hands as h
import chuckleClasses as ch
from settings import *

class Card(pygame.sprite.Sprite):

    RANK = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    SUIT = ["Hearts", "Diamonds", "Spades", "Clubs"]

    def __init__(self, sprites, x, y, rank, suit):
        super(Card, self).__init__()
        self.selectable = False
        self.back = pygame.transform.scale(sprites["Back"], (100, 150))
        self.front = pygame.transform.scale(sprites[suit][rank], (100, 150))
        self.image = self.front
        self.rect = self.image.get_rect()
        self.selected = False
        self.defaultPos = (x, y)

    def update(self):
        if self.selected:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.center = self.defaultPos

    def click(self):
        if self.selectable:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                if not self.selected:
                    self.selected = True
                else:
                    self.selected = False

class Deck(h.Deck):
    def __init__(self, sprites):
        super(Deck, self).__init__()
        self.sprites = sprites


    def createDeck(self):
        j = 0
        for suit in Card.SUIT:
            j += 1
            i = 1
            for rank in Card.RANK:
                i += 1
                card = Card(self.sprites, i * 100, j * 150, rank, suit)
                self.addCard(card)

class Player(ch.Player):
    def __init__(self, name, pos, rot):
        super(Player, self).__init__(name)



