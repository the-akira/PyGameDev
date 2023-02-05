import numpy as np
import pygame

pygame.init()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mandelbrot')

def mandelbrot(c, max_iterations=80):
    z = c
    for n in range(max_iterations):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iterations

grid = np.zeros((height, width), dtype=int)
for i in range(height):
    for j in range(width):
        c = complex(-2 + 3.0 * j / width, -1 + 2.0 * i / height)
        grid[i, j] = mandelbrot(c)

grid = np.interp(grid, (grid.min(), grid.max()), (0, 255))

for i in range(height):
    for j in range(width):
        color = (int(grid[i, j]) + 1) % 256
        pygame.draw.rect(screen, (0, color, 0), (j, i, 1, 1))

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()