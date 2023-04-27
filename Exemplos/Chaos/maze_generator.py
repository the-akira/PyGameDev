import pygame
import random

# Define the maze parameters
maze_width = 20
maze_height = 20
cell_size = 20

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((maze_width * cell_size, maze_height * cell_size))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

# Define the colors
bg_color = (255, 255, 255)
line_color = (0, 0, 0)

# Create the maze
maze = [[0 for x in range(maze_width)] for y in range(maze_height)]
visited = [[False for x in range(maze_width)] for y in range(maze_height)]

# Define the directions
directions = ["N", "E", "S", "W"]
delta = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

def in_bounds(x, y):
    return x >= 0 and x < maze_width and y >= 0 and y < maze_height

def generate_maze(x, y):
    visited[y][x] = True
    random.shuffle(directions)
    for direction in directions:
        dx, dy = delta[direction]
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and not visited[ny][nx]:
            if direction == "N":
                maze[y][x] |= 1
                maze[ny][nx] |= 4
            elif direction == "E":
                maze[y][x] |= 2
                maze[ny][nx] |= 8
            elif direction == "S":
                maze[y][x] |= 4
                maze[ny][nx] |= 1
            else:
                maze[y][x] |= 8
                maze[ny][nx] |= 2
            generate_maze(nx, ny)

# Generate the maze
generate_maze(0, 0)

# Draw the maze
def draw_maze():
    screen.fill(bg_color)
    for y in range(maze_height):
        for x in range(maze_width):
            cell = maze[y][x]
            x1, y1 = x * cell_size, y * cell_size
            x2, y2 = (x + 1) * cell_size, (y + 1) * cell_size
            if not (cell & 1): # N
                pygame.draw.line(screen, line_color, (x1, y1), (x2, y1))
            if not (cell & 2): # E
                pygame.draw.line(screen, line_color, (x2, y1), (x2, y2))
            if not (cell & 4): # S
                pygame.draw.line(screen, line_color, (x2, y2), (x1, y2))
            if not (cell & 8): # W
                pygame.draw.line(screen, line_color, (x1, y2), (x1, y1))

draw_maze()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
    clock.tick(60)