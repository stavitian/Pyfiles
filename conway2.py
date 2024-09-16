import pygame
import numpy as np
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
width, height = 1000, 1000
cell_size = 10
cols, rows = width // cell_size, height // cell_size
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BUTTON_COLOR = (0, 128, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

# Crear una matriz para la grilla
grid = np.zeros((rows, cols), dtype=int)

def draw_grid():
    for x in range(0, width, cell_size):
        for y in range(0, height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            if grid[y // cell_size, x // cell_size] == 1:
                pygame.draw.rect(screen, WHITE, rect)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)

def update_grid():
    global grid
    new_grid = np.copy(grid)
    for r in range(rows):
        for c in range(cols):
            total = np.sum(grid[max(0, r-1):min(rows, r+2), max(0, c-1):min(cols, c+2)])
            if grid[r, c] == 1:
                total -= 1
                if total < 2 or total > 3:
                    new_grid[r, c] = 0
            elif total == 3:
                new_grid[r, c] = 1
    grid = new_grid

def draw_button():
    button_rect = pygame.Rect(width - 150, height - 50, 140, 40)
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render('Random Grid', True, WHITE)
    screen.blit(text, (width - 140, height - 45))

def generate_random_grid():
    global grid
    grid = np.zeros((rows, cols), dtype=int)
    # Generar patrones aleatorios interesantes
    for _ in range(rows * cols // 4):  # Proporción para mantener la grilla entretenida
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        grid[y, x] = 1

# Bucle principal
running = True
paused = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if width - 150 <= x <= width - 10 and height - 50 <= y <= height - 10:
                generate_random_grid()
            else:
                grid[y // cell_size, x // cell_size] = 1 - grid[y // cell_size, x // cell_size]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        update_grid()

    screen.fill(BLACK)
    draw_grid()
    draw_button()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
