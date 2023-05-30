from tipchyk import Races, Tip4yk
import random
import math

class Fero_world:
    def __init__(self, size) -> None:
        self.grid = [[{'black': 0.0, 'white': 0.0, 'yellow': 0.0, 'orange': 0.0} for _ in range(size)] for _ in range(size)]

    def add_phero(self, tip, world):
        if tip.race == Races.BLACK:
            self.grid[tip.cords[0]][tip.cords[1]]['black'] += tip.energy/100
        if tip.race == Races.WHITE:
            self.grid[tip.cords[0]][tip.cords[1]]['white'] += tip.energy/100
        if tip.race == Races.ORANGE:
            self.grid[tip.cords[0]][tip.cords[1]]['orange'] += tip.energy/100
        if tip.race == Races.YELLOW:
            self.grid[tip.cords[0]][tip.cords[1]]['yellow'] += tip.energy/100

    def clear_phero(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                self.grid[i][j]['black'] *= 0.7
                self.grid[i][j]['white'] *= 0.7
                self.grid[i][j]['yellow'] *= 0.7
                self.grid[i][j]['orange'] *= 0.7
