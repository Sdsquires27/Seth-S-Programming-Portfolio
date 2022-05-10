## Seth Squires, 
## The Oregon Trail
## 10.21

### imports ###
import random

import math

from oregonArt import *

playing = True
creator = "Seth Squires and Daniel Chavez"
tm = "2021"


# functions #

def splash_screen():
    print(LOGO)
    print("\t\t" + creator)
    print("\t\t" + tm)


def menus(options):
    global choice
    while True:
        print(RIBBON)
        # repeats the length of the previously inputted options
        for i in range(len(options)):
            # prints the number that we are on as well as the number of options we are on.
            print(str.format("\t{0}   {1:<30}", i + 1, options[i]))
        print(RIBBON)

        choice = input("What would you like to do? ")

        # If the choice is a number and it is within the range of numbers
        if choice.isnumeric():
            if int(choice) <= len(options):
                choice = int(choice)
                return choice

            else:
                print("That's not an option!")
        else:
            print("That's not an option!")


def game_menu():
    global playing
    global choice
    while True:

        print(TITLE)

        menus(["Travel the trail", "Learn about the trail", "End"])
        if choice == 1:
            return choice

        elif choice == 2:
            print("info about the trail.")
            print("press enter to proceed to the next piece of information")
            for i in range(len(OREGONINFO)):
                input(OREGONINFO[i])
        elif choice == 3:
            playing = False
            return playing


def classMenu():
    global type
    global money
    while True:
        print("Many kinds of people made the trip to Oregon. \nYou may:")

        menus(["Be a banker from Boston", "Be a carpenter from Ohio", "Be a farmer from Illinois",
               "Find out the differences between these choices."])

        print(RIBBON)
        if choice == 1:
            type = "Banker"
            money = 2000
            return money
        elif choice == 2:
            type = "Carpenter"
            money = 1000
            return money
        elif choice == 3:
            type = "Farmer"
            money = 500
            return money
        elif choice == 4:
            print("Information about the classes")
            print("Press enter to continue to the next piece of information")
            # repeat for the length of the tuple, wait until the user hits enter
            for i in range(len(CLASSINFO)):
                input(CLASSINFO[i])
            print(RIBBON)


def askName(question):
    global name
    while True:
        name = input(question)
        # If the name is all letters or the length is zero, go on.
        if name.isalpha() or len(name) == 0:
            break
        else:
            print("That's not a valid option. Letters only.")
    return name


def nameMenu(money):
    global names
    global name
    names = []
    fillIn = False
    partySize = 0

    while int(partySize) > 5 or int(partySize) < 3:
        partySize = input("How many people would you like to journey with? 3-5 ")
        if partySize.isnumeric():
            if int(partySize) > 5 or int(partySize) < 3:
                print("Please enter a valid response.")
        else:
            partySize = 0
            print("Please enter a valid response")


    # repeats length of party
    for i in range(int(partySize)):
        # If you haven't already hit enter
        if not fillIn:
            askName("Enter a name ")

            # if the length of your input is 0, fills it in with random names Otherwise puts in whatever you put in.
            if len(name) == 0:
                fillIn = True
                names.append(random.choice(NAMES))
            else:
                names.append(name)

        # If you have already hit enter, continue doing random names.
        else:
            names.append(random.choice(NAMES))

    # Looking to figure out if the names are correct. Repeats until you say yes.
    correct = "N"

    while correct[0] != "Y":
        for i in range((len(names))):
            print(names[i])

        correct = input("Are these names correct? ")


        while len(correct) == 0:
            print("Please enter a valid response.")
            correct = input("Are these names correct? ")

        correct = correct.upper()

        if correct[0] == "N":
            changeName = True
            while changeName:
                change = input("Which name is incorrect? ")
                # sees if the input is numeric and if it is a valid number, or if it is within the list of names
                if (change.isnumeric() and int(change) - 1 <= len(names) and int(change) - 1 >= 0) or (change in names):

                    # If the name is in the list of names, list the number that it is
                    if change in name:
                        change = name.index(change)

                    # Find the new name that they are looking for. Still has the autofill option.
                    askName("What would you like this name to change to? ")
                    if len(name) == 0:
                        names[int(change) - 1] = random.choice(NAMES)
                        changeName = False
                    else:
                        names[int(change) - 1] = name
                        changeName = False
                else:
                    print("Please enter a valid number, or the exact name.")
            else:
                print("Please enter a valid response.")

    if "Elon musk" in names:
        money += 1000000000
    return names, money


# def naming():
#     while True:
#
#         invalid = True
#         while invalid:
#             nameLeader = input("What is the first name of the wagon leader?")
#             if len(nameLeader) == 0:
#                 nameLeader = random.choice(NAMES)
#                 name2 = random.choice(NAMES)
#                 name3 = random.choice(NAMES)
#                 name4 = random.choice(NAMES)
#                 name5 = random.choice(NAMES)
#                 invalid = False
#
#             elif (nameLeader.isalpha()):
#                 invalid = False
#             else:
#                 print("That is not a valid input. Letters only.")
#
#         invalid = True
#         while invalid:
#             name2 = input("What is the name of the second traveller?")
#             if len(name2) == 0:
#                 name2 = random.choice(NAMES)
#                 name3 = random.choice(NAMES)
#                 name4 = random.choice(NAMES)
#                 name5 = random.choice(NAMES)
#                 invalid = False
#
#             elif (name2.isalpha()):
#                 invalid = False
#             else:
#                 print("That is not a valid input. Letters only.")
#
#         invalid = True
#         while invalid:
#             name3 = input("What is the name of the third traveller?")
#             if len(name3) == 0:
#                 name3 = random.choice(NAMES)
#                 name4 = random.choice(NAMES)
#                 name5 = random.choice(NAMES)
#                 invalid = False
#
#             elif (name3.isalpha()):
#                 invalid = False
#             else:
#                 print("That is not a valid input. Letters only.")
#
#         invalid = True
#         while invalid:
#             name4 = input("What is the name of the fourth traveller?")
#             if len(name4) == 0:
#                 name4 = random.choice(NAMES)
#                 name5 = random.choice(NAMES)
#                 invalid = False
#
#             elif (name4.isalpha()):
#
#                 invalid = False
#             else:
#                 print("That is not a valid input. Letters only.")
#
#         invalid = True
#
#         while invalid:
#             name5 = input("What is the name of the final traveller?")
#             if len(name5) == 0:
#                 name5 = random.choice(NAMES)
#                 invalid = False
#
#             elif (name5.isalpha()):
#                 invalid = False
#             else:
#                 print("That is not a valid input. Letters only.")
#         print(nameLeader)
#         print(name2)
#         print(name3)
#         print(name4)
#         print(name5)
#         correct = input("Are these names correct?")
#         correct = correct.upper()
#         if correct[0] == "Y":
#             namesWrong = False


def monthMenu():
    while True:
        print(
            "It is 1848. Your jumping off place for Oregon is Independence,Missouri.  You must decide which month to leave Independence.:")

        # run menu function
        menus(["March", "April", "May", "June", "July", "Ask for advice."])

        # set month to answer
        print(RIBBON)
        inMenu = False
        if choice == 1:
            startMonth = 3
            return startMonth
        elif choice == 2:
            startMonth = 4
            return startMonth
        elif choice == 3:
            startMonth = 5
            return startMonth
        elif choice == 4:
            startMonth = 6
            return startMonth
        elif choice == 5:
            startMonth = 7
            return startMonth
        elif choice == 6:
            print("Ask for advice.")
            print("Press enter to continue to the next piece of information")
            for i in range(len(MONTHINFO)):
                input(MONTHINFO[i])



def shopMenu(oxen, food, clothing, ammo, money, partsInventory):
    bill = 0
    parts_bill = 0.00
    partsInventory = []
    choices = ["Oxen", "Food", "Clothes", "Ammunition", "Wagon Parts", "Check Out"]
    spentOnItems = [0.00, 0.00, 0.00, 0.00, 0.00, bill]
    
    print("Before leaving Independence you should buy Equipment and Supplies")
    print(str.format("You have ${:.2f} in cash to make this trip", money))
    print("Remember you can buy supplies along the way so you don't have to spend it all now")
    input("Press any Key to Continue")

    while True:

        spentOnItems[len(spentOnItems)-1] = bill
        print("Welcome to the General Store")
        print("Here is a list of things you can buy")
        print(RIBBON)
        print()
        for i in range(len(choices)):
            print(str.format("\t{:<2}: {:<20}  ${:<.2f}", i+1, choices[i], spentOnItems[i]))

        print(str.format("Total Bill so far:    \t\t  ${:.2f}",bill))
        print(str.format("Total funds available:\t\t  ${:.2f}",money-bill))

        print(RIBBON)

        choice = input("What item would you like to buy?")
        if choice.isnumeric():
            choice = int(choice)
        else:
            print("Please enter a valid number.")

        if choice == 1:
            while True:
                bill -= spentOnItems[0]
                oxen = 0
                spentOnItems[0] = 0.00
                print("""
                There are 2 oxen in a yoke;
                I recommend at least 3 yokes.
                I charge $40 a yoke
                """)

                print(str.format("Total Bill so far:    \t\t  ${}", bill))
                answer = input("How many yoke do you want")

                if answer.isnumeric():
                    answer = int(answer)
                    break
                else:
                    print("Please enter a valid number.")

            cost = answer*40
            oxen = answer*2
            bill += cost
            spentOnItems[0] = cost


        elif choice == 2:
            while True:
                bill -= spentOnItems[1]
                food = 0
                spentOnItems[1] = 0.00

                print("""
                I recommend you take at
                least 200 pounds of food
                for each person in your
                family. I see that you have
                5 people in all. You'll need 
                flour, sugar, bacon, and
                coffee. My price is 20
                cents a pound.
                """)

                print(str.format("Total Bill so far:    \t\t  ${}", bill))
                answer = input("How many pounds of food do you want")

                if answer.isnumeric():
                    answer = int(answer)
                    break
                else:
                    print("Please enter a valid number.")

            cost = answer * .2
            food = answer
            bill += cost
            spentOnItems[1] = cost

        elif choice ==3:
            bill -= spentOnItems[2]
            clothing = 0
            spentOnItems[2] = 0.00
            print("""
            You'll need warm clothing in the mountains.
            I recommend Taking at least 2 sets of clothiers per person.
            Each set its $10.00
            """)

            print(str.format("Total Bill so far:    \t\t  ${}", bill))
            answer = input("How many sets of clothes do you want")

            if answer.isnumeric():
                answer = int(answer)
            else:
                print("Please enter a valid number.")

            cost = answer * 2
            clothing = answer * 1
            bill += cost
            spentOnItems[2] = cost

        elif choice ==4:
            bill -= spentOnItems[3]
            ammo = 0
            spentOnItems[3] = 0.00
            print("""
            I sell ammunition in boxes of 20 bullets. Each box costs $2.00
            """)

            print(str.format("Total Bill so far:    \t\t  ${}", bill))
            answer = input("How many boxes do you want")

            if answer.isnumeric():
                answer = int(answer)
            else:
                print("Please enter a valid number.")

            cost = answer * 2
            ammo = answer * 20
            bill += cost
            spentOnItems[3] = cost

        elif choice == 5:
            print("""
                It is a good idea to have a few
                Spare parts for your wagon on hand
                you never know what can happen on
                the trail and a broken down
                wagon can be a death sentence.
            """)
            partsInventory = []
            bill -= parts_bill
            parts = ["Wagon Wheel", "Wagon axle", " Wagon tongue", " Back to main Shop"]
            parts_cost = [10.00, 20.00, 50.00, parts_bill]
            while True:
                parts_cost[len(parts_cost)- 1] = parts_bill

                for i in range(len(parts)):
                    print(str.format("\t{:<2}: {:<20}  ${:<.2f}", i+1, parts[i], parts_cost[i]))

                print(str.format("Current inventory: {}", partsInventory))
                print(str.format("Total Bill so far:    \t\t  ${:.2f}", bill))
                print(str.format("Total funds available:\t\t  ${:.2f}", money - bill))

                parts_choice = input("What is your choice")

                if parts_choice.isnumeric():
                    parts_choice = int(parts_choice)
                else:
                    print("Please enter a valid number.")

                if parts_choice == 1:

                    while "Wagon wheel" in partsInventory:
                        partsInventory.remove("Wagon wheel")
                        parts_bill -= parts_cost[0]

                    answer = int(input("How many wagon wheels do you want?"))
                    for i in range(answer):
                        partsInventory.append("Wagon wheel")
                    parts_bill += parts_cost[0] * answer

                elif parts_choice == 2:

                    while "Wagon axle" in partsInventory:
                        partsInventory.remove("Wagon axle")
                        parts_bill -= parts_cost[1]

                    answer = int(input("How many wagon axles do you want?"))
                    for i in range(answer):
                        partsInventory.append("Wagon axle")
                    parts_bill += parts_cost[1] * answer

                elif parts_choice == 3:

                    while "Wagon tongue" in partsInventory:
                        partsInventory.remove("Wagon tongue")
                        parts_bill -= parts_cost[2]

                    answer = int(input("How many wagon tongues do you want?"))
                    for i in range(answer):
                        partsInventory.append("Wagon tongue")
                    parts_bill += parts_cost[2] * answer

                elif parts_choice == 4:
                    bill+= parts_bill
                    spentOnItems[4] = parts_bill
                    break
                else:
                    print("Something went wrong")

        elif choice == 6:
            if bill <= money:
                money -= bill
                return oxen, food, clothing, ammo, money, partsInventory
            else:
                print("I'm sorry but I can't give credit. Come back when you're a little richer.")
                input("Press enter to continue")
        else:
            print("Something went wrong")
            print(choice)


## Old Code ##
##    global playing
##

##    in_menu = True
##    while in_menu:
##        print (TITLE)
##        print(RIBBON)
##        print("1.\t travel the trail")
##        print("2.\t Learn about the trail")
##        print("3.\t END")
##        choice= input("what is your choice? ")
##        if choice == ("1"):
##            print ("travel")
##        elif choice== ("2"):
##            print("info about the trail")
##            for i in range(len(INFO)):
##            
##                print(INFO[i])
##                input("Press enter to continue")
##                      
##        elif choice == ("3"):
##            in_menu =False
##            playing = False
##        else:
##            print("not a good choice")

def changePace():
    pace = 0
    while True:
        # create the menu that tells you what everything does
        choice = menus(["A steady pace", "A strenuous pace", "A grueling pace", "Find out what different paces mean"])

        #set the pace based on your answer
        if choice == 1:
            pace = 1
            break
        elif choice == 2:
            pace = 2
            break
        elif choice == 3:
            pace = 3
            break

            #info
        elif choice == 4:
            print("Steady- you travel about 9 hours a day taking frequent rest. you take good care to not get too tired\n",
                  "Strenuous - you travel about 12 hours a day, starting just after sunrise and stopping shortly before sunset. You stop to\n",
                  "Grueling- You travel about 16 hours a day, Starting before sunrise and continuing until dark.You almost never stop to rest, you do not get enough sleep at night. You finish each day exhausted, and your health suffers.")
            input("Press enter to continue.")
    return pace

def hunt(ammo, food):
    gain = 0
    if ammo > 0:
        num = random.randint(0, 100)
        if num > 30:
            gain += random.randint(10,50)
            ammo -= random.randint(1,20)
            print("You got some food!")
            input("Press enter to continue.")

        else:
            gain = 0
            ammo -= random.randint(1, 20)
            print("You didn't manage to catch anything.")
            input("Press enter to continue.")

    else:
        print("You are an idiot, How are you going to go hunt with out bullets, not only your crew is hungry but you wasted the whole day for nothing.")

    if ammo < 0:
        ammo = 0
    food += gain

    return food, ammo





def trade(oxen, clothing, ammo, food, partsInventory):

    wagonWheel = 0
    wagonTongue = 0
    wagonAxle = 0
    for i in range(len(partsInventory)):
        if partsInventory[i] == "Wagon wheel":
            wagonWheel += 1
        elif partsInventory[i] == "Wagon axle":
            wagonAxle += 1
        elif partsInventory[i] == "Wagon tongue":
            wagonTongue += 1

    print(" Your supplies ")
    choices = ["Oxen", "Food", "Clothes", "Ammunition", "Wagon wheels", "Wagon axles", "Wagon tongues",]
    supplies = [oxen, food, clothing, ammo, wagonWheel, wagonAxle, wagonTongue]
    
    for i in range(len(choices)):
        print(str.format("\t{:<20} {:>10}", choices[i], supplies[i]))

    # fifty percent chance of being able to trade at all
    num = random.randint(0, 1)
    if num == 0:
        # picks random option from list
        item = random.randint(1, len(choices))-1
        theirItem = random.randint(1, len(choices))-1

        itemName = choices[item]
        # if their item is the same as yours, it makes it not the same.
        if theirItem == item:
            theirItem -= 1
            if theirItem < 0:
                theirItem = len(choices)-1

        theirItemName = choices[theirItem]

        # picks a random amount of the item they want
        amount = random.randint(1,4)
        theirAmount = random.randint(1,4)

        # If they want food, increases the amount they want

        # if itemName == "Food" or "Ammunition":
        #     amount = amount*20
        # if theirItemName == "Food" or "Ammunition":
        #     theirAmount = theirAmount*20

        print(str.format("You meet another emigrant who wants {} {}. He will trade you {} {}.", amount, itemName,
                         theirAmount, theirItemName))

        if amount > supplies[item]:
            print("You don't have enough.")
            input("Press enter to continue ")
        else:
            willing = input("Are you willing to trade? ")


            while len(willing) == 0:
                print("Please enter a valid response.")
                correct = input("Are you willing to trade? ")

                willing = willing.upper()
                #oxen, food, clothing, ammo, wagonWheel, wagonAxle, wagonTongue

            if willing[0] == "Y":
                # remove your item
                if item == 0:
                    oxen -= amount
                elif item == 1:
                    food -= amount
                elif item == 2:
                    clothing -= amount
                elif item == 3:
                    ammo -= amount
                elif item == 4:
                    wagonWheel -= amount
                elif item == 5:
                    wagonTongue -= amount
                elif item == 6:
                    wagonAxle -= amount

                # add their item
                if item == 0:
                    oxen += theirAmount
                elif item == 1:
                    food += theirAmount
                elif item == 2:
                    clothing += theirAmount
                elif item == 3:
                    ammo += theirAmount
                elif item == 4:
                    wagonWheel += theirAmount
                elif item == 5:
                    wagonTongue += theirAmount
                elif item == 6:
                    wagonAxle += theirAmount




                print(partsInventory)
                return oxen, clothing, ammo, food, wagonWheel, wagonAxle, wagonTongue







    else:
        print("There's no one to trade")
        input("press enter to continue")



def changeRations(rations):
    print("Current rations:"+str(rations))
    choice = menus(["Filling -- meals are large and generous.", "meager -- meals are small, but adequate.",
                    "bare bones --meals are very small; everyone stays hungry."])
    if choice == 1:
        rations = 1
    elif choice == 2:
        rations = .5
    elif choice == 3:
        rations = .25
    return rations

def pickIllness(health):
    choice = random.randint(1, 10)
    if choice == 1:
        choice2 = names[random.randint(1,len(names))-1]
        choice=random.choice(ILLNESS)
        print(choice2, "caught", choice)
        input("Press enter to continue")
        health -= 35
    return health


def displaySupplies(oxen, clothing, ammo, money, food, partsInventory):
    wagonWheel = 0
    wagonTongue = 0
    wagonAxle = 0
    for i in range(len(partsInventory)):
        if partsInventory[i] == "Wagon wheel":
            wagonWheel += 1
        elif partsInventory[i] == "Wagon axle":
            wagonAxle += 1
        elif partsInventory[i] == "Wagon tongue":
            wagonTongue += 1

    print(" Your supplies ")
    choices = ["Oxen", "Food", "Clothes", "Ammunition", "Wagon wheels", "Wagon axles", "Wagon tongues", "Money Left"]
    supplies = [oxen, food, clothing, ammo, wagonWheel, wagonAxle, wagonTongue, money]

    for i in range(len(choices)):
        print(str.format("\t{:<20} {:>10}", choices[i], supplies[i]))



def displayTravelScreen(health, pace, rations, milesTravelled, length, food, clothing, broke, brokeDown, day, startMonth):
    # updates everything
    print(RIBBON)
    #date
    if day > 30:
        day = 1
        startMonth += 1

    # Weather
    weatherType = "Good"
    weather = random.randint(1,3)
    if weather == 1:
        weatherType = "Good"
    elif weather == 2:
        weather = .25
        weatherType = "Rainy"
    elif weather == 3:
        weather = .5
        weatherType = "Hot"

    # food
    food -= 3*rations*len(names)
    if food < 0:
        health = 0
        food = 0

    # health
    if weather == .5:
        if clothing < len(names):
            health - 10
    if weather == .25:
        if clothing < len(names):
            health - 25
# lose health. Increases based on less rations and faster pace
    #health -= 5/rations*pace

    healthType = "Good"
    if health >= 80:
        healthType = "Good"
    elif health >= 50:
        healthType = "Poor"
    elif health > 0:
        healthType = "Very Poor"
    else:
        dead = random.randint(0, len(names)-1)
        print(names[dead], "has died")
        input("Press enter to continue")
        names.pop(dead)
        health = 100

    # break part
    num = random.randint(1,100)
    if num < 7:
        brokeDown = True
        num = random.randint(1,3)
        if num == 1:
            broke = "Wagon wheel"
        elif num ==2:
            broke = "Wagon tongue"
        elif num ==3 :
            broke = "Wagon axle"


    paceType = "Steady"
    if pace == 1:
        paceType = "Steady"
    elif pace == 2:
        paceType = "Strenuous"
    else:
        paceType = "Grueling"

    print("Date:", startMonth, "/", day)
    print("Weather:", weatherType)
    print("Health:", healthType)
    print("Pace:", paceType)
    print("Miles left: ", length - milesTravelled)
    print("Food remaining:", food)
    return weather, food, broke, brokeDown, day, startMonth, health

def travel(oxen, weather, health, pace, money, milesTravelled, clothes, ammo, food):
    if random.randint(0,1) == 1:

        choice = random.randint(1,6)
        if choice == 3:
            lose = random.randint(100, 1000)
            if lose > money:
                lose = money
                money -= lose
            print(str.format("you got robbed by 3 teenagers and lost ${} money", lose)) # -$1000 or whatever money you have left
        if choice == 2:
            print("you got lost, lose one day")
        if choice == 1:
            gain = random.randint(100,1000)
            money += gain
            print(str.format("you won the lottery and you won ${}", gain))
        if choice == 4:
            oxen -= 1
            print("your oxen died of boredom") # loose 1 oxen
        if choice == 5:
            health -= 25
            print("one of your passengers threw up") # loose 25 health

        if choice == 6:
            clothes -= len(names)
            if clothes < 0:
                clothes = 0
            health -= 20
            ammo -= 20
            if ammo < 0:
                ammo = 0
            food += 50
            print("You went the wrong path and got attacked by a group of purple dinosaurs.")  #

    miles = math.ceil(oxen*2*weather*pace)
    print(str.format("You travelled {} miles today.", miles))
    input("Press Enter to Continue")
    milesTravelled += miles
    return milesTravelled, health, oxen, money, clothes, ammo, food





### Main ###

def main():
    global playing
    # def variables
    playing = True
    type = None
    food = 0
    oxen = 0
    clothing = 0
    ammo = 0
    parts = []
    startMonth = ""
    health = 100
    day = 1
    date = startMonth + "/" + str(day)
    weather = 1
    partyCondition = 1
    pace = 1
    rations = 1
    travelOptions = ["Continue on Trail", "Check supplies", "Change Pace", "Change Ration", "Rest", "Trade", "Hunt"]
    totalLength = 2200
    milesTravelled = 0
    names = []
    brokeDown= False
    money = 0
    partsInventory = []
    broke = None


    # display splash screen
    splash_screen()
    input("Press enter to continue")
    while playing:


        # Start the game
        game_menu()
        if not playing:
            break

        print(RIBBON)

        # Choose your class (banker, carpenter, or farmer)
        money = classMenu()

        # choose your names
        names, money = nameMenu(money)
        print(names)

        # choose what month you want to start at
        startMonth = monthMenu()

        # Shop
        oxen, food, clothing, ammo, money, partsInventory = shopMenu(oxen, food, clothing, ammo, money, partsInventory)
        #print(oxen, food, clothing, ammo, money, partsInventory)

        # Travel the trail
        while (milesTravelled < totalLength) and len(names) >= 1:

            health = pickIllness(health)

            weather,food,broke, brokeDown, day,startMonth, health = displayTravelScreen(health, pace, rations, milesTravelled, totalLength, food, clothing, broke, brokeDown,day, startMonth)

            choice = menus(travelOptions)
            if choice == 1:
                #travel
                if oxen >= 1 and not brokeDown:
                    day += 1
                    milesTravelled, health, oxen, money, clothing,ammo,food = travel(oxen, weather, health, pace, money, milesTravelled,clothing,ammo,food)
                else:
                    print("Can't travel at this time")
                    if oxen < 1:
                        print("You have no oxen")
                    else:
                        # if something is broken, you try to fix it. If that doesn't work, you need a replacement part.
                        print("You are broke down. You need a "+broke)
                        input("You try to fix it yourself. Press enter to continue.")
                        num = random.randint(1,100)
                        if num < 20:
                            broke = None
                            brokeDown = False
                            print("You fixed it!")
                        else:
                            if broke in partsInventory:
                                print("You have to use a replacement part.")
                                for i in range(len(partsInventory)):
                                    if partsInventory[i] == broke:
                                        num = i
                                partsInventory.pop(num)
                            else:
                                print("You don't have a replacement part. You won't be able to travel until you get one.")

                    continue
            elif choice == 2:
                #show supplies
                displaySupplies(oxen, clothing, ammo, money, food, partsInventory)
                continue
            elif choice == 3:
                # change pace
                pace = changePace()
            elif choice == 4:
                # change rations
                rations = changeRations(rations)
            elif choice == 5:
                # increase day by one, increase health up to the max health
                day += 1
                health += 25
                if health > 100:
                    health = 100
            elif choice == 6:
                # trade
                oxen, clothing, ammo, food, wagonWheel, wagonAxle, wagonTongue = trade(oxen, clothing, ammo, food, partsInventory)

                # attempt to fix the unpacking problem... didn't work
                partsInventory.clear()

                for i in range(wagonWheel):
                    partsInventory.append("Wagon wheel")
                for i in range(wagonAxle):
                    partsInventory.append("Wagon axle")
                for i in range(wagonTongue):
                    partsInventory.append("Wagon tongue")

            elif choice == 7:
                # hunt
                food, ammo = hunt(ammo, food)
                day += 1



        ## End ##
        if totalLength <= milesTravelled:
            print("Good job you made it to Oregon")
            break
        else:
            print("your choice cost your family their lives")
            break







    print("Game Over")


main()
# money = 2000
# oxen = 0
# food = 0
# clothes = 0
# ammo = 0
# parts = []
#
# shopMenu(money,oxen,food,clothes,ammo,parts)

input()
