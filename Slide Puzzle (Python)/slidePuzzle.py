# Seth Squires
# Christmas
# 12-21
from tkinter import *
from functools import partial
import random



class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.height = 1080
        self.width = 1920
        self.buttons = []
        self.sequence = 0
        self.grid()
        self.createUI()

    def createUI(self):
        self.master.title("Slide Puzzle")
        self.master.geometry("1280x800")
        self.master.attributes("-fullscreen", True)
        self.master.bind("x", quit)

        img = PhotoImage(file="bg.png")
        self.bg = Label(self, image=img)
        self.bg.image = img
        self.bg.place(x=0, y=0)
        self.pack(fill=BOTH, expand=1)


        self.open_lbl = Label(self,
                              text="Slide Puzzler",
                              fg="black",
                              font=("Castellar", 80),
                              bg="#8cfffb"
                              )
        self.open_lbl.place(x=550, y=0)

        self.start_btn = Button(self, text="Start", width=8, height=2, font=("SimSun", 30),
                                command=self.startProgramOnClick, bg="black", fg="white")
        self.start_btn.place(x=800, y=300)

        self.items = [self.open_lbl, self.start_btn, self.bg]

    def startProgramOnClick(self):
        self.proceed()
        #self.makeSlidePuzzle([["WHITE", "BLUE", "GREEN"], ["BLACK", "MAGENTA", "YELLOW"], ["CYAN", "RED", "ORANGE"]],

        #                     [["BLACK", "CYAN", "RED"], ["BLUE", "YELLOW", "GREEN"], ["MAGENTA", "ORANGE", "WHITE"]])

    def proceed(self):

        for i in range(len(self.buttons)):
            for i2 in range(len(self.buttons[i])):
                self.buttons[i][i2].destroy()
        start = [["WHITE", "BLUE", "GREEN"], ["BLACK", "MAGENTA", "YELLOW"], ["CYAN", "RED", "ORANGE"]]
        end = self.generateRandomPuzzle(start)

        # start and end are flipped because the start is where you want to end up and the end is where the board begins.
        # I don't know why.
        self.makeSlidePuzzle(start=start, end=end, position=[0, 2])
        self.drawGoal(end)

    def drawGoal(self, end):
        for i in range(len(end)):
            for i2 in range(len(end[i])):
                x = Button(fg=end[i][i2], bg=end[i][i2], width=10, height=4)
                x.place(x=1500 + 75*i, y=800 + 75*i2)

    def generateRandomPuzzle(self, start):

        # generates completely random boards, then tests to see if they would actually work
        for row in start:
            random.shuffle(row)

        random.shuffle(start)

        return start

    def destroyItems(self):

        for i in range(len(self.items)):
            self.items[i].destroy()
        for i in range(len(self.items)):
            self.items.pop(0)





    def gridMove(self, name):

        xPos = 0
        yPos = 0

        for i in range(len(self.colors)):
            if name in self.colors[i]:
                xPos = i
                for i2 in range(len(self.colors[i])):
                    if self.colors[i][i2] == name:
                        yPos = i2
                        break

        # checks that either the x position is equal to the other white position and there is only one difference in y,
        # or that the y position is equal and there is only one difference in x

        if (xPos == self.whitePos[0] and (yPos+1 == self.whitePos[1] or yPos-1 == self.whitePos[1])) or \
                (yPos == self.whitePos[1] and (xPos+1 == self.whitePos[0] or xPos-1 == self.whitePos[0])):
            print("This is a valid move")


            self.colors[xPos][yPos] = "WHITE"
            self.colors[self.whitePos[0]][self.whitePos[1]] = name

            print(self.whitePos)

            # replaces the current button's command with the white button's command
            self.buttons[xPos][yPos]['command'] = partial(self.gridMove, "WHITE")
            self.buttons[self.whitePos[0]][self.whitePos[1]]['command'] = partial(self.gridMove, name)

            self.buttons[xPos][yPos]['bg'] = "WHITE"
            self.buttons[self.whitePos[0]][self.whitePos[1]]['bg'] = name

            self.buttons[xPos][yPos]['fg'] = "WHITE"
            self.buttons[self.whitePos[0]][self.whitePos[1]]['fg'] = name

            self.buttons[xPos][yPos]['text'] = "WHITE"
            self.buttons[self.whitePos[0]][self.whitePos[1]]['text'] = name

            tempButton = self.buttons[xPos][yPos]


            self.whitePos = [xPos, yPos]

            print(self.colors)
            if self.colors == self.end:

                print("You won!")
                self.proceed()


        elif xPos == self.whitePos[0] and yPos == self.whitePos[1]:
            print("this is the white button")

        else:
            print("This is an invalid move")

        # if xPos != len(self.buttons)-1:
        #     print("This button is not on the very right")
        #     if "WHITE" in self.colors[xPos+1]:
        #         print("White is to the right of this button")
        #
        # if xPos != 0:
        #     print("This button is not on the very left")
        #     if "WHITE" in self.colors[xPos-1]:
        #         print("White is to the left of this button")
        #
        # if yPos != len(self.buttons[0])-1:
        #     print("This button is not at the very bottom")
        #     for i in range(len(self.colors)):
        #         if self.colors[i][yPos-1] == "WHITE":
        #             print("WHITE is above this button")
        #
        # if yPos != 0:
        #     print("This button is not at the very top")
        #     for i in range(len(self.colors)):
        #         if self.colors[i][yPos+1] == "WHITE":
        #             print("WHITE is below this button")


    def makeSlidePuzzle(self, start=None, end=None, position=None):

        if self.items is not None:
            self.destroyItems()

        if start is None:
            start = [["WHITE", "RED", "YELLOW"], ["BLUE", "BLACK", "MAGENTA"], ["CYAN", "GREEN", "ORANGE"]]


        if end is None:
            self.end = [["MAGENTA", "YELLOW", "CYAN"], ["GREEN", "WHITE", "BLUE"], ["BLACK", "RED", "ORANGE"]]
        else:
            self.end = end

        if position is None:
            self.whitePos = [0, 0]
        else:
            self.whitePos = position

        self.buttons = []
        self.colors = []

        for i in range(len(start)):
            self.buttons.append([])
            self.colors.append([])
            for i2 in range(len(start[i])):


                self.id = [i, i2]
                self.colors[i].append(start[i][i2])
                self.buttons[i].append(Button(text=start[i][i2], fg=start[i][i2], bg=start[i][i2], width=40, height=16,
                                              command=partial(self.gridMove, start[i][i2])))
                self.buttons[i][i2].place(x=(i*300)+300, y=i2*300)
        print(self.colors)











def main():
    root = Tk()
    Application(root)
    root.mainloop()


main()
