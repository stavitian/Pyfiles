import numpy as np
from vpython import *
import random

# Configuración inicial
size = 20
cells = np.zeros((size, size, size))

# Crear escena que ocupe toda la ventana
scene = canvas(title='Juego de la Vida de Conway 3D Mejorado', width=900, height=900)
scene.append_to_caption('\n\n')  # Espacio para los controles

# Ajustar la cámara
scene.camera.pos = vector(size/2, size/2, size*2)
scene.camera.axis = vector(-size/2, -size/2, -size*2)
scene.userzoom = True
scene.userspin = True

# Función para generar colores basados en la posición Z
def get_color(z):
    return vector(z/size, 0.5, 1 - z/size)

# Inicialización de voxels
voxels = [[[None for _ in range(size)] for _ in range(size)] for _ in range(size)]

# Variables para reglas personalizables
survival_min = 4
survival_max = 6
birth_count = 4

def initialize_grid():
    global cells, voxels
    cells = np.random.choice([0, 1], size=(size, size, size), p=[1-initial_density.value, initial_density.value])
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
                    if survival_min <= neighbors <= survival_max:  # Regla de supervivencia
                        new_cells[x][y][z] = 1
                else:
                    if neighbors == birth_count:  # Regla de nacimiento
                        new_cells[x][y][z] = 1
    
    cells = new_cells
    update_voxels()

# UI para controles
def reset_button_pressed(b):
    initialize_grid()

button(bind=reset_button_pressed, text='Reiniciar', pos=scene.title_anchor)

running = True
def toggle_pause(b):
    global running
    running = not running
    b.text = 'Reanudar' if not running else 'Pausar'

pause_button = button(bind=toggle_pause, text='Pausar', pos=scene.title_anchor)

# Controles para modificar reglas
scene.append_to_caption('\n\nDensidad inicial: ')
initial_density = slider(min=0, max=1, step=0.1, value=0.3, bind=None)

scene.append_to_caption('\n\nRegla de supervivencia:\n')
scene.append_to_caption('Mínimo de vecinos: ')
survival_min_slider = slider(min=1, max=26, step=1, value=survival_min, bind=None)
scene.append_to_caption('Máximo de vecinos: ')
survival_max_slider = slider(min=1, max=26, step=1, value=survival_max, bind=None)

scene.append_to_caption('\n\nRegla de nacimiento:\n')
scene.append_to_caption('Número de vecinos para nacer: ')
birth_count_slider = slider(min=1, max=26, step=1, value=birth_count, bind=None)

def update_rules(ev):
    global survival_min, survival_max, birth_count
    survival_min = int(survival_min_slider.value)
    survival_max = int(survival_max_slider.value)
    birth_count = int(birth_count_slider.value)

button(text="Aplicar Reglas", bind=update_rules)

# Inicialización
initialize_grid()

# Bucle principal
while True:
    rate(4)  # Actualizamos 10 veces por segundo
    if running:
        update()