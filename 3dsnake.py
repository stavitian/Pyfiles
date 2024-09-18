import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import pygame_gui

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL | RESIZABLE)
pygame.display.set_caption('3D Snake Game')

# Initialize OpenGL
gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -15)

# Snake parameters
snake = [(0, 0, 0)]
direction = (1, 0, 0)
score = 0

# Food parameters
food = (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

# GUI manager
manager = pygame_gui.UIManager((800, 600))

# Sliders for viewport angle and zoom
angle_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 10), (200, 20)), start_value=45, value_range=(10, 120), manager=manager)
zoom_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 40), (200, 20)), start_value=-15, value_range=(-50, -5), manager=manager)

# Camera parameters
camera_pos = [0.0, 0.0, -15.0]
camera_rot = [0.0, 0.0]

# Game loop
running = True
clock = pygame.time.Clock()

def draw_cube(x, y, z, color):
    vertices = (
        (x - 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y - 0.5, z - 0.5),
        (x + 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y + 0.5, z - 0.5),
        (x - 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y - 0.5, z + 0.5),
        (x + 0.5, y + 0.5, z + 0.5),
        (x - 0.5, y + 0.5, z + 0.5)
    )
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    )
    glColor3fv(color)
    glBegin(GL_QUADS)
    for surface in edges:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

font = pygame.font.SysFont(None, 36)

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                direction = (0, 0, -1)
            elif event.key == K_e:
                direction = (0, 0, 1)
            elif event.key == K_w:
                direction = (0, 1, 0)
            elif event.key == K_s:
                direction = (0, -1, 0)
            elif event.key == K_a:
                direction = (-1, 0, 0)
            elif event.key == K_d:
                direction = (1, 0, 0)
            elif event.key == K_UP:
                if pygame.key.get_mods() & KMOD_SHIFT:
                    camera_rot[0] += 5
                else:
                    camera_pos[2] += 1
            elif event.key == K_DOWN:
                if pygame.key.get_mods() & KMOD_SHIFT:
                    camera_rot[0] -= 5
                else:
                    camera_pos[2] -= 1
            elif event.key == K_LEFT:
                if pygame.key.get_mods() & KMOD_SHIFT:
                    camera_rot[1] += 5
                else:
                    camera_pos[0] -= 1
            elif event.key == K_RIGHT:
                if pygame.key.get_mods() & KMOD_SHIFT:
                    camera_rot[1] -= 5
                else:
                    camera_pos[0] += 1
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), DOUBLEBUF | OPENGL | RESIZABLE)
            glViewport(0, 0, event.w, event.h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(angle_slider.get_current_value(), (event.w / event.h), 0.1, 50.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(*camera_pos)
            glRotatef(camera_rot[0], 1, 0, 0)
            glRotatef(camera_rot[1], 0, 1, 0)
        manager.process_events(event)

    manager.update(time_delta)

    # Move snake
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1], head[2] + direction[2])
    snake.insert(0, new_head)

    # Check if snake eats food
    if new_head == food:
        score += 1
        food = (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    else:
        snake.pop()

    # Wrap around the edges
    for i in range(len(snake)):
        x, y, z = snake[i]
        snake[i] = (x % 10, y % 10, z % 10)

    # Clear screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Update OpenGL perspective and zoom based on sliders
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(angle_slider.get_current_value(), (screen.get_width() / screen.get_height()), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(*camera_pos)
    glRotatef(camera_rot[0], 1, 0, 0)
    glRotatef(camera_rot[1], 0, 1, 0)

    # Draw snake
    for segment in snake:
        draw_cube(*segment, (0, 1, 0))  # Green color for snake

    # Draw food
    draw_cube(*food, (1, 0, 0))  # Red color for food

    # Draw GUI
    manager.draw_ui(screen)

    # Draw score text
    score_text = f"Score: {score}"
    draw_text(score_text, font, (255, 255, 255), screen, 10, screen.get_height() - 40)

    # Update display
    pygame.display.flip()
    clock.tick(5)

pygame.quit()
