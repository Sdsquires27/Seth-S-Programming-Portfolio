# Seth Squires
# 1/22
# Blackjack

import commonGameFunctions as cgf
from chuckleClasses import *

def main():
    print("\t\tWelcome to Chucklehead!\n")
    names = []
    numPlayers = cgf.getNumInRange(2, 4, "How many players? (2-4): ")
    for i in range(numPlayers):
        names.append(cgf.getName())

    game = ChuckleGame(names)
    again = None
    while again != "No":
        game.play()
        again = cgf.askYesOrNo("\nDo you want to play again?")



main()
