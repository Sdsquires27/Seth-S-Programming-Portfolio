from settings import *


class Button(pg.sprite.Sprite):
    # I *think* that this button can be used universally. You just need a game class with certain settings
    def __init__(self, game, x, y, function):
        # settings for pygame
        self._layer = UI_LAYER
        self.groups = game.ui
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # create images
        self.unselectedImg = self.game.buttonImages[0]
        self.selectedImg = self.game.buttonImages[1]
        self.image = self.unselectedImg

        # set up rect and pos
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


        # declare function to be run when clicked
        self.function = function

    def update(self):
        self.image = self.unselectedImg

        # if you have a function
        if self.function:
            # if mouse collision
            x, y = pg.mouse.get_pos()
            if self.rect.collidepoint(x, y):

                # test to see if clicked
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.click()

                self.image = self.selectedImg

    def click(self):
        # run function
        if self.function:
             self.function()
