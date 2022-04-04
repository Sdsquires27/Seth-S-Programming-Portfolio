class Card(object):

    RANK = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUIT = ["♥", "♦", "♠", "♣"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit



    def __str__(self):
        rep = str.format("""
        __________
        | {0}{1}     |
        |        |
        |        |
        |        |
        |     {1}{0} |
        |________|
        """, self.rank, self.suit)
        return rep


class PositionalCard(Card):
    def __init__(self, rank, suit):
        super(PositionalCard, self).__init__(rank, suit)
        self.flippedUp = False

    def flipCard(self):
        self.flippedUp = not self.flippedUp


    def __str__(self):
        if self.flippedUp:
            rep = super(PositionalCard, self).__str__()

        else:
            rep = str.format("""
            __________
            |♥♦♠♣♥♦♠|
            |♦♠♣♥♦♠♣|
            |♠♣♥♦♠♣♥|
            |♣♥♦♠♣♥♦|
            |♥♦♠♣♥♦♠|
            |--------|
            """)

        return rep


if __name__ == "__main__":
    print("This is not a program. Try importing and using the classes.")
    input("\n\nPress the enter key to exit.")

