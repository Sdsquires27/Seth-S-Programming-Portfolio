from card import *
import commonGameFunctions as cgf

class Hand(object):

    def __init__(self):
        self.cards = []

    def __str__(self):
        rep = ""
        lines = []
        if self.cards:
            for i in range(len(self.cards)):
                lines.append([])
                for line in self.cards[i].__str__().splitlines(False):
                    lines[i].append(line)

            for i in range(len(lines[0]) - 1):
                for i2 in range(len(lines)):
                    rep += lines[i2][i]
                rep += "\n"



            # for i in self.cards:
            #     lines.append([])
            #     for line in (self.cards[i].__str__().splitlines(False)):
            #         lines[i].append(line)



        else:
            rep = "<EMPTY>"

        return rep

    def addCard(self, card):
        self.cards.append(card)


    def giveCard(self, card, other_hand):
        self.cards.remove(card)
        other_hand.addCard(card)

    def clear(self):
        self.cards.clear()


class Deck(Hand):


    def createDeck(self):
        for suit in Card.SUIT:
            for rank in Card.RANK:
                card = PositionalCard(rank, suit)
                self.addCard(card)

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands_list, perHand=1):

        for i in range(perHand):
            for hand in hands_list:
                topCard = self.cards[0]
                self.giveCard(topCard, hand)


if __name__ == "__main__":
    print("This is not a program. Try importing and using the classes.")
    input("\n\nPress the enter key to exit.")


