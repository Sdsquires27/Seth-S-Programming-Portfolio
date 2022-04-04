# Seth Squires
# 11/21
# Common Game Functions


# askYesOrNo
def askYesOrNo(question):
    """asks a yes or no question to the user and returns the answer if it is yes or no"""
    while True:
        answer = input(question)

        if ("y" in answer.lower() and "n" in answer.lower()):
            print("\nThat answer was too complicated for me. Try again. \n")
            continue
        elif ("y" in answer.lower()):
            answer = "Yes"
            return answer
        elif ("n" in answer.lower()):
            answer = "No"
            return answer
        else:
            print("\nInvalid response. Try again.\n")

# flip coin, roll dice
def flipCoin():
    import random
    """picks a random value and returns heads or tails"""
    side = random.randint(0, 1)
    if side == 0:
        side = "Heads"
        return side
    elif side == 1:
        side = "Tails"
        return side

def rollDice(high):
    import random
    """takes in the number of sides and picks a random number"""
    side = random.randint(1, high)
    return side

# getNumInRange
def getNumInRange(low, high, question):
    """"takes in a minimum, maximum and question. Asks the user the question, then gets the answer and returns it."""
    while True:
        number = input(question)
        try:
            number = int(number)
            if number >= low:
                if number <= high:
                    return number

                else:
                    print("Too high, try again.\n")
            else:
                print("Too low, try again.\n")
        except:
            print("Invalid input, try again.\n")

# Make a menu and return an input
def menu(text, options):
    """takes in a list of options and asks the player which they would like to do."""
    print(text)
    while True:
        for i in range(len(options)):
            print(str(i+1)+" "+options[i])
        answer = input("What would you like to do? ")
        try:
            answer = int(answer)
            if answer <= len(options) and answer > 0:
                return answer-1
            else:
                input("Invalid input, press enter to try again.\n")


        except:
            input("Invalid input, press enter try again.\n")

def getName():
    """asks the user for their name and returns it."""
    while True:
        name = input("What's your name?")
        if name.isalpha() and len(name)>0:
            name.capitalize()
            return name
        else:
            input("Invalid input, press enter to try again.")

def shuffleDeck(deck):
    """takes a deck and shuffles it."""
    import random
    random.shuffle(deck)
    return deck

def dealCard(deck):
    """takes in a deck and gives the top part of that deck"""
    card = deck.pop(0)
    return card

def randomCard(deck):
    """takes in a deck and gives a random card from that deck"""
    import random
    card = deck.pop(random.randint(0,len(deck)-1))
    return card

if __name__ == "__main__":
    print("This is not a program. Try importing and using the classes.")
    input("\n\nPress the enter key to exit.")
