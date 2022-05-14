from settings import *
import os

class Map:
    def __init__(self, folder):
        folder = os.listdir(folder)
        self.maps = []
        self.mapNames = []
        for i in range(len(folder)):
            file = os.path.join(lvlFolder, folder[i])
            self.maps.append([])
            with open(file, "rt") as f:
                for line in f:
                    self.maps[i].append(line.strip())

        self.background = self.maps.pop(0)
