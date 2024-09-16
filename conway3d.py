import numpy as np
from vpython import *
import random

# Configuración
size = 30
cells = np.zeros((size, size, size))

# Crear escena
scene = canvas(title='Juego de la Vida de Conway 3D Mejorado', width=800, height=600)
scene.camera.pos = vector(size/2, size/2, size*2)
scene.camera.axis = vector(-size/2, -size/2, -size*2)

# Función para generar colores basados en la posición Z
def get_color(z):
    return vector(z/size, 0.5, 1 - z/size)

# Inicialización de voxels
voxels = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]

def initialize_grid():
    global cells, voxels
    cells = np.random.choice([0, 1], size=(size, size, size))
    update_voxels()

def update_voxels():
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if cells[x][y][z] == 1:
                    if voxels[x][y][z] is None:
                        voxels[x][y][z] = box(pos=vector(x, y, z), 
                                              size=vector(0.8,0.8,0.8), 
                                              color=get_color(z))
                    else:
                        voxels[x][y][z].visible = True
                elif voxels[x][y][z] is not None:
                    voxels[x][y][z].visible = False

def count_neighbors(x, y, z):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                nx, ny, nz = (x+dx)%size, (y+dy)%size, (z+dz)%size
                count += cells[nx][ny][nz]
    return count

def update():
    global cells
    new_cells = np.zeros((size, size, size))
    for x in range(size):
        for y in range(size):
            for z in range(size):
                neighbors = count_neighbors(x, y, z)
                if cells[x][y][z] == 1:
                    if 4 <= neighbors <= 6:  # Regla de supervivencia
                        new_cells[x][y][z] = 1
                else:
                    if neighbors == 4:  # Regla de nacimiento
                        new_cells[x][y][z] = 1
    
    cells = new_cells
    update_voxels()

# Crear botón para reiniciar
def reset_button_pressed(b):
    initialize_grid()

button(bind=reset_button_pressed, text='Reiniciar', pos=scene.title_anchor)

# Inicialización
initialize_grid()

# Variables para control de pausa
running = True

def toggle_pause(b):
    global running
    running = not running
    b.text = 'Reanudar' if not running else 'Pausar'

pause_button = button(bind=toggle_pause, text='Pausar', pos=scene.title_anchor)

# Configuración para rotación de cámara
scene.userzoom = True
scene.userspin = True

# Bucle principal
while True:
    rate(10)  # Actualizamos 10 veces por segundo
    if running:
        update()