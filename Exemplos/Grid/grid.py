import pygame, sys
pygame.init()

size = (width, height) = 600, 600
win = pygame.display.set_mode(size)
pygame.display.set_caption('Grid Example')
cols, rows = 25, 25
w = width//cols
h = height//rows

class Cell:
    def __init__(self, i, j):
        self.x, self.y = i, j
   
    def show(self, win, color):
        pygame.draw.rect(win, color, (self.x*w, self.y*h, w-2, h-2))

grid = []
for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Cell(i, j))
    grid.append(arr)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for i in range(cols):
        for j in range(rows):
            cell = grid[j][i]
            cell.show(win, (255, 255, 255)) 

    pygame.display.flip()