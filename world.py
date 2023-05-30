
import numpy as np
import pygame
import time
import random
from havka import Havka, Cluster, Havka_world 
from tipchyk import States, Races, Tip4yk
from fero import Fero_world

class World:
    def __init__(self, size, people) -> None:
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self.day = 0
        self.phero = Fero_world(size)
        for line in people:
            for person in line:
                self.grid[person.cords[0]][person.cords[1]] = person
        self.havka = Havka_world(self.size, 4)

    def add_tip(self, tipanya):
        if random.random() > 0.5:
            self.grid[tipanya.cords[0]][tipanya.cords[1]] = tipanya

    def cut_grid(self):
        for i in range(10):
            for index, line in enumerate(self.grid):
                self.grid[index][i] = 0
                self.grid[index][-(i+1)] = 0
        for j in range(5):
            self.grid[j] = [0 for _ in range(self.size)]
        for j in range(1, 6):
            self.grid[-j] = [0 for _ in range(self.size)]


    def run_day(self):
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.grid[i][j], Tip4yk):
                    self.grid[i][j].run(self)
        self.havka.day += 1
        self.day += 1
        self.phero.clear_phero()

    def __str__(self):
        return str('\n'.join(str(line) for line in self.grid))