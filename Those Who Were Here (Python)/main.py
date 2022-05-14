# Pygame template - skeleton for a new pygame project
from game import *

g = Game()
g.showStartScreen()
while g.running:
    g.new()

pygame.quit()
