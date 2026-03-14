import os
import pygame

# set up asset folders
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder, "img")
cardFolder = os.path.join(imgFolder, "Cards")
sndFolder = os.path.join(gameFolder, "snd")

fontArial = pygame.font.match_font("arial")

chuckleRules = \
["The rules of Chucklehead are as follows:",
    "If you don't already know how to play, give up",
    "Each player takes a turn playing one card.",
    "You can only play a card of higher or equal value than the card before it.",
    "If a seven if played, the next card must be of equal or lower value than the seven.",
    "Ten's clear the pile.",
    "Two's can be played on any card.",
    "If you can not play a card, you must take the pile and end your turn.",
    "If you have less than three cards at the end of your turn, you take the top card of the deck and add it to your main hand.",
    "If four of the same card are played in a row, the pile is cleared and the player gets to go again.",
    "You have three hands: a main hand, a hand of cards facing up, and a hand of cards facing down.",
    "You can play multiple cards of the same value at once from your main hand.",
    "Upon running out of cards in one hand, you can begin to play cards in the next hand.",
    "When playing cards facing down, you must play blind. If the card cannot be played, you must take the pile.",
    "If you are out of cards, you win!"]

WIDTH = 1600
HEIGHT = 800
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



