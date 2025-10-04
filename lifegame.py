import sys
import random
import time
from copy import deepcopy
from OpenGL.GL import *
from OpenGL.GLUT import *

#defining the parameters of the grid
WIDTH = 64      # number of pixels horizontally
HEIGHT = 48     # number of pixels vertically
CELL_SIZE = 10  # cell size in OpenGL
FPS = 30 # Updates/ second

SPECIES = ['red', 'green', 'blue']
UPDATE_INTERVAL = 1.0 / FPS

# mapping rgb colors
COLOR_MAP = {
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'blue': (0.0, 0.0, 1.0),
    '.': (0.0, 0.0, 0.0)
}

# Initialize random grid
grid = [[random.choice(SPECIES + ['.']) for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Count neighbors for species
def count_neighbors(x, y, species):
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % WIDTH, (y + dy) % HEIGHT
            if grid[ny][nx] == species:
                count += 1
    return count

# Update grid for next generation
def update_grid():
    global grid
    new_grid = deepcopy(grid)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            for species in SPECIES:
                neighbors = count_neighbors(x, y, species)
                if grid[y][x] == species:
                    new_grid[y][x] = species if neighbors in (2, 3) else '.'
                elif grid[y][x] == '.':
                    if neighbors == 3:
                        new_grid[y][x] = species
    grid = new_grid

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            species = grid[y][x]
            glColor3f(*COLOR_MAP[species])
            glBegin(GL_QUADS)
            glVertex2f(x*CELL_SIZE, y*CELL_SIZE)
            glVertex2f((x+1)*CELL_SIZE, y*CELL_SIZE)
            glVertex2f((x+1)*CELL_SIZE, (y+1)*CELL_SIZE)
            glVertex2f(x*CELL_SIZE, (y+1)*CELL_SIZE)
            glEnd()
    glutSwapBuffers()

# Timer callback
def timer(value):
    update_grid()
    glutPostRedisplay()
    glutTimerFunc(int(1000/FPS), timer, 0)

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH*CELL_SIZE, HEIGHT*CELL_SIZE)
    glutCreateWindow(b"Multi-Species Game of Life")
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WIDTH*CELL_SIZE, 0, HEIGHT*CELL_SIZE, -1, 1)
    glutDisplayFunc(display)
    glutTimerFunc(int(1000/FPS), timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
