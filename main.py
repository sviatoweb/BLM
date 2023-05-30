
import numpy as np
import pygame
import time
import random
from havka import Havka, Cluster, Havka_world 
from tipchyk import States, Races, Tip4yk
from fero import Fero_world
from world import World



def visualize(world,havka_world, CELL_SIZE, GAP_SIZE, WINDOW_SIZE, window):
    grid_width = world.size * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
    grid_height = world.size * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
    grid_surface = pygame.Surface((grid_width, grid_height))
    grid_surface.fill(Races.BLACK)
    for i in range(havka_world.size):
        for j in range(havka_world.size):
            cell = havka_world.grid[i][j]
            color = None
            if isinstance(cell, Havka):
                if cell.is_ready(havka_world.day):
                    color = Races.GREEN
                else:
                    color = (100,100,100)
            else:
                color = (100,100,100)
            cell_x = j * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
            cell_y = i * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
            pygame.draw.rect(grid_surface, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
    for i in range(world.size):
        for j in range(world.size):
            cell = world.grid[i][j]
            color = None
            if isinstance(cell, Tip4yk):
                color = cell.race
            else:
                continue
            cell_x = j * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
            cell_y = i * (CELL_SIZE + GAP_SIZE) + GAP_SIZE
            pygame.draw.rect(grid_surface, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
    scaled_surface = pygame.transform.scale(grid_surface, WINDOW_SIZE)
    window.blit(scaled_surface, (0, 0))
    pygame.display.flip()

def main(size):
    WINDOW_SIZE = (700, 700)
    CELL_SIZE = 40
    GAP_SIZE = 0
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Cell Life Simulator")   
    world = World(size, [[Tip4yk([12, 17, 29, 22], Races.BLACK,[0+i, 0+i],100) for i in range(8)],
                        [Tip4yk([24, 16, 16, 16], Races.WHITE,[size - 1 - i, size - 1 - i],100) for i in range(8)],
                        [Tip4yk([11, 24, 12, 7], Races.YELLOW,[0 + i,size - 1 - i],100) for i in range(8)],
                        [Tip4yk([19, 14, 22, 28], Races.ORANGE,[size - 1 - i, 0 + i],100) for i in range(8)]])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        visualize(world,world.havka, CELL_SIZE, GAP_SIZE, WINDOW_SIZE, window)
        world.run_day()
    pygame.quit()

main(100)