import os
import pygame
from grid_class import Grid  # your Grid class here
from particle_types import PARTICLE_TYPES

pygame.init()

# Window setup
width, height = 1400, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("py_sandbox")

# Constants
PARTICLE_SCALE = 4
FPS = 60

# Colors (for background)
BG_COLOR = (30, 30, 30)

# Grid setup
grid = Grid(height, width, PARTICLE_SCALE, 0.5)

# Clock for framerate control
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse input — add particle on left click
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // PARTICLE_SCALE
        grid_y = mouse_y // PARTICLE_SCALE

        # Example: alternate between sand, water, gas
        grid.add_particle(grid_x, grid_y, 'sand')  # swap 'sand' to any p_type you want to test

    # Update simulation
    grid.update_grid()

    # Draw
    screen.fill(BG_COLOR)

    for x in range(grid.width):
        for y in range(grid.height):
            particle = grid.contents[x][y]
            if particle != 0:
                pygame.draw.rect(
                    screen,
                    particle.color,
                    (x * PARTICLE_SCALE, y * PARTICLE_SCALE, PARTICLE_SCALE, PARTICLE_SCALE)
                )

    pygame.display.flip()

pygame.quit()
