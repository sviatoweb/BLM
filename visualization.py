from main import *
import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Font settings
font_size = 32
font = pygame.font.SysFont(None, font_size)

# Function to draw organisms on the screen
def draw_organisms(organisms):
    organism_width = 20
    organism_height = 20
    padding = 10

    x = padding
    y = padding

    for index, generation in enumerate(organisms):
        # Render the generation text
        generation_text = font.render(f"Generation {index}", True, WHITE)
        text_rect = generation_text.get_rect(center=(screen_width // 2, 20))
        screen.blit(generation_text, text_rect)

        sum_genomes = 0
        for organism in generation:
            pygame.draw.rect(screen, organism._color, (random.randint(20, 780), random.randint(35, 550), organism_width, organism_height))
            sum_genomes += sum(organism._genome)
            x += organism_width + padding
        generation_text = font.render(f"Avarage sum of genes {round(sum_genomes/ 26, 2)}", True, WHITE)
        text_rect = generation_text.get_rect(center=(screen_width // 2, 40))
        screen.blit(generation_text, text_rect)
        x = padding
        y += organism_height + padding

        pygame.display.flip()
        screen.fill(BLACK)
        pygame.time.wait(1000)




# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    draw_organisms(populations)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
