from collections import deque
import pygame, sys

pygame.init()
SIZE = (WIDTH, HEIGHT) = 640, 480
win = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Dijkstra's Path Finding Algorithm")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()
FPS = 65

cols, rows = 64, 48
w = WIDTH // cols
h = HEIGHT // rows
grid = []
queue = deque()
visited = []
path = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 254, 106)
BLUE = (64, 206, 227)
GREEN = (21, 82, 24)
PURPLE = (117, 48, 201)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    win.blit(img, (x, y))

class Cell:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False

    def show(self, win, color, shape=1):
        if self.wall == True:
            color = BLACK
        if shape == 1:
            pygame.draw.rect(win, color, (self.x * w, self.y * h, w - 1, h - 1))
        else:
            pygame.draw.circle(win, color, (self.x * w + w // 2, self.y * h + h // 2), w // 3)

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])

def create_wall(pos, state):
    x, y = pos
    i = x // w
    j = y // h
    if grid[i][j] != start and grid[i][j] != end:
        grid[i][j].wall = state

for i in range(cols):
    array = []
    for j in range(rows):
        array.append(Cell(i, j))
    grid.append(array)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

start = grid[cols // 2][rows // 2]
end = grid[cols - 50][rows - cols // 2]
start.wall = False
end.wall = False

flag = False
noflag = True
startflag = False

queue.append(start)
start.visited = True

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not startflag:
            if pygame.mouse.get_pressed()[0]:
                create_wall(pygame.mouse.get_pos(), True)
            if pygame.mouse.get_pressed()[2]:
                create_wall(pygame.mouse.get_pos(), False)
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    create_wall(pygame.mouse.get_pos(), True)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                startflag = True

    for i in range(cols):
        for j in range(rows):
            cell = grid[i][j]
            cell.show(win, WHITE)
            if cell in path:
                cell.show(win, YELLOW)
            elif cell.visited:
                cell.show(win, BLUE)
            if cell in queue:
                cell.show(win, WHITE)
                cell.show(win, BLUE, 0)
            if cell == start:
                cell.show(win, GREEN)
            if cell == end:
                cell.show(win, PURPLE)

    if startflag:
        if len(queue) > 0:
            current = queue.popleft()
            if current == end:
                temp = current
                while temp.prev:
                    path.append(temp.prev)
                    temp = temp.prev
                if not flag:
                    flag = True
                elif flag:
                    continue
            if not flag:
                for i in current.neighbors:
                    if not i.visited and not i.wall:
                        i.visited = True
                        i.prev = current
                        queue.append(i)
        else:
            if noflag and not flag:
                noflag = False
                pygame.time.wait(2000)
                win.fill(BLACK)
                draw_text('Não há solução!', font, WHITE, (WIDTH // 2) - 80, HEIGHT // 2 - 10)
            else:
                continue

    pygame.display.flip()