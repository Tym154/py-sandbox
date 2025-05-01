import os
import pygame
from grid_class import Grid
from particle_types import PARTICLE_TYPES

pygame.init()

# Window setup
width, height = 1200, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("py_sandbox")

# Constants
PARTICLE_SCALE = 16
void_density = 0.5
FPS = 60
BG_COLOR = (30, 30, 30)

# Grid setup
grid = Grid(height, width, PARTICLE_SCALE, 0.5, void_density)

# Clock for framerate control
clock = pygame.time.Clock()

# Materials
materials = ['discard','metal', 'water', 'sand', 'smoke']
selected_material = materials[0]

# Brush control
brush_size = 1
max_brush_size = 10

# Button layout
button_height = 40
button_width = 120
button_margin = 10

def get_button_rects():
    rects = []
    for idx, mat in enumerate(materials):
        button_x = button_margin + idx * (button_width + button_margin)
        button_y = button_margin
        rect = pygame.Rect(button_x, button_y, button_width, button_height)
        rects.append((rect, mat))
    return rects

def draw_buttons(button_rects):
    for rect, mat in button_rects:
        color = (70, 70, 70)
        if mat == selected_material:
            color = (150, 150, 150)
        pygame.draw.rect(screen, color, rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(mat, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

# Precompute button rects once
button_rects = get_button_rects()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for rect, mat in button_rects:
                if rect.collidepoint(mouse_x, mouse_y):
                    selected_material = mat
                    break

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > button_height + button_margin * 2:
            grid_x = mouse_x // PARTICLE_SCALE
            grid_y = mouse_y // PARTICLE_SCALE

            half_brush = brush_size // 2
            for dx in range(-half_brush, half_brush + 1):
                for dy in range(-half_brush, half_brush + 1):
                    px = grid_x + dx
                    py = grid_y + dy
                    if 0 <= px < grid.width and 0 <= py < grid.height:
                        if selected_material == 'discard':
                            grid.contents[px][py] = 0
                        else:
                            grid.add_particle(px, py, selected_material)
                        

    grid.update_grid()

    screen.fill(BG_COLOR)

    draw_buttons(button_rects)

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
