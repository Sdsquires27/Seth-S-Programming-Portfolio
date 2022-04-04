import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, sprites, x, y):
        super(Card, self).__init__()
        self.image = pygame.transform.scale(sprites["Back"], (100, 150))
        self.rect = self.image.get_rect()
        self.selected = False
        self.defaultPos = (x, y)

    def update(self):
        if self.selected:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.center = self.defaultPos

    def click(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            if not self.selected:
                self.selected = True
            else:
                self.selected = False


