import hands as h
import card as c
import commonGameFunctions as cgf


class Player(object):
    def __init__(self, name):
        self.name = name
        self.upCards = ChuckleHand()
        self.downCards = ChuckleHand()
        self.hand = ChuckleHand()
        self.currentHand = self.hand


class ChuckleDeck(h.Deck):

    def createDeck(self):
        for suit in c.Card.SUIT:
            for rank in c.Card.RANK:
                card = ChuckleCard(rank, suit)
                self.addCard(card)


class ChuckleHand(h.Hand):

    def flipCards(self):
        for card in self.cards:
            card.flippedUp = True

    def hideHand(self):
        for card in self.cards:
            card.flippedUp = False

class ChuckleDiscard(ChuckleHand):
    def __str__(self):
        self.flipCards()
        if self.cards:
            rep = self.cards[len(self.cards) - 1].__str__()
        else:
            rep = "None"
        return rep

    @property
    def value(self):
        if self.cards:
            v = self.cards[len(self.cards) - 1].value
        else:
            v = 0
        return v


    def fourInRow(self):
        inRow = True
        print(len(self.cards))
        if len(self.cards) >= 4:
            v = self.cards[len(self.cards) - 1].value
            for i in range(4):
                if self.cards[len(self.cards) - (1 + i)].value != v:
                    inRow = False
        else:
            inRow = False

        return inRow

class ChuckleCard(c.PositionalCard):
    ACE_VALUE = 14

    @property
    def value(self):
        if self.flippedUp:
            v = ChuckleCard.RANK.index(self.rank) + 1

            if v == 1:
                v = ChuckleCard.ACE_VALUE


        else:
            v = None

        return v


# this is used for a non-graphical game only
class ChuckleGame(object):
    # this is used for a non-graphical project only

    def __init__(self, names):
        self.playerList = []
        for name in names:
            player = Player(name)
            self.playerList.append(player)

        self.turn = 0

        self.discard = ChuckleDiscard()

        self.deck = ChuckleDeck()
        self.deck.createDeck()
        self.deck.shuffle()
        self.winner = None

        self.playing = True
        self.explode = False



    # note that the play function is intended for console only play. This program has been adapted for graphical play
    def play(self):
        # deal out cards

        # three to each face down
        decks = []
        for player in self.playerList:
            decks.append(player.downCards)
        self.deck.deal(decks, 3)

        # three to each face up
        decks = []
        for player in self.playerList:
            decks.append(player.upCards)
        self.deck.deal(decks, 3)


        # three to each in hand
        decks = []
        for player in self.playerList:
            decks.append(player.hand)
        self.deck.deal(decks, 3)


        while self.playing:
            if self.turn % len(self.playerList) == 0 and not self.explode:
                if self.turn != 0:
                    print(str.format("END OF ROUND {}", self.turn // len(self.playerList)))
                    input("Press enter to continue")

                if self.deck.cards:
                    print("Deck length: ", len(self.deck.cards))
                for player in self.playerList:
                    player.upCards.flipCards()
                    player.hand.flipCards()
                    print(player.name.upper() + ":")
                    print("Face down:")
                    print(player.downCards)
                    print("Face up:")
                    print(player.upCards)
                    player.hand.hideHand()
                    print("Hand:")
                    print(player.hand)
                    player.hand.flipCards()
                    input("Press enter to continue\n")

            self.explode = False

            print("Discard:")
            print(self.discard, "\n")

            curPlayer = self.playerList[self.turn % len(self.playerList)]
            print(curPlayer.name+"'s turn!")
            input("Press enter to continue")

            # Player takes turn
            if curPlayer.hand.cards:
                curPlayer.currentHand = curPlayer.hand
                print("Hand:")

            elif curPlayer.upCards.cards:
                curPlayer.currentHand = curPlayer.upCards
                print("Face Up (Hand out):")

            else:
                curPlayer.currentHand = curPlayer.downCards
                print("Face Down (Hand and Face up out):")


            print(curPlayer.currentHand)
            input("Press enter to continue")

            # Player plays a card.
            turnGoing = True
            while turnGoing:

                options = []
                for card in curPlayer.currentHand.cards:
                    options.append(card.__str__())

                options.append("Take the discard pile and end turn")
                if self.discard.value == 7:
                    choice = cgf.menu("Which card would you like to play? (must be lower on sevens)", options)
                else:
                    choice = cgf.menu("Which card would you like to play?", options)

                # It must be higher or equal in value than the one before it, unless special rules apply.
                if choice != len(options) - 1:
                    selCard = curPlayer.currentHand.cards[choice]
                    if selCard.value is None:
                        selCard.flipCard()
                        print(selCard)

                    print(selCard.value)
                    print(self.discard.value)

                    if self.discard.value != 7 and (not selCard.value >= self.discard.value and selCard.value != 2):
                        print("Card is too low, cannot be played")
                        input("Press enter to continue")

                        if curPlayer.currentHand == curPlayer.downCards:
                            curPlayer.currentHand.giveCard(selCard, curPlayer.hand)
                            for i in range(len(self.discard.cards)):
                                self.discard.giveCard(self.discard.cards[0], curPlayer.hand)
                            turnGoing = False

                    elif self.discard.value == 7 and (not selCard.value <= self.discard.value):
                        print("Card is too high (must be lower on sevens), cannot be played")
                        input("Press enter to continue")
                        if curPlayer.currentHand == curPlayer.downCards:
                            curPlayer.currentHand.giveCard(selCard, curPlayer.hand)
                            for i in range(len(self.discard.cards)):
                                self.discard.giveCard(self.discard.cards[0], curPlayer.hand)
                            turnGoing = False

                    else:
                        # If there are multiples cards:
                        if curPlayer.currentHand == curPlayer.hand:
                            multiples = False
                            multList = []
                            for card in curPlayer.currentHand.cards:
                                if card.value == selCard.value and card != selCard:
                                    multiples = True
                                    multList.append(card)

                            if multiples:
                                num = cgf.getNumInRange(0, len(multList), str.format(
                                    "You have {} additional copies of this value, how many would you like to play?",
                                    len(multList)))
                                for i in range(num):
                                    curPlayer.currentHand.giveCard(multList[i], self.discard)

                        curPlayer.currentHand.giveCard(selCard, self.discard)
                        print("Card played!")
                        input("Press enter to continue")

                        # Check for special events
                        if self.discard.fourInRow():
                            self.discard.clear()
                            print("Four in a row! Discard pile removed, play again!")
                            input("Press enter to continue")
                            self.turn -= 1
                            self.explode = True

                        if selCard.value == 10:
                            self.discard.clear()
                            print("Ten played! Discard pile removed, play again!")
                            input("Press enter to continue")
                            self.turn -= 1
                            self.explode = True

                        if self.discard.cards and \
                                (curPlayer.currentHand == curPlayer.hand and len(curPlayer.hand.cards) < 3):
                            if self.deck.cards and curPlayer.hand.cards:
                                self.deck.giveCard(self.deck.cards[0], curPlayer.hand)
                        if not curPlayer.hand.cards and not curPlayer.upCards.cards and not curPlayer.downCards.cards:
                            self.playing = False
                            self.winner = curPlayer



                        turnGoing = False


                else:

                    for i in range(len(self.discard.cards)):
                        self.discard.giveCard(self.discard.cards[0], curPlayer.hand)
                    turnGoing = False

                # If player is unable to play a card, takes the discard pile and ends turn.

            self.turn += 1

        print(self.winner.name + " wins!")
        input("Press enter to continue.")
