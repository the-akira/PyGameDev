import pygame
import math
import heapq

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

# Grid dimensions
GRID_WIDTH = 800
GRID_HEIGHT = 600
CELL_SIZE = 20
NUM_ROWS = GRID_HEIGHT // CELL_SIZE
NUM_COLS = GRID_WIDTH // CELL_SIZE

screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption('A* Algorithm')

# Node class to represent each cell in the grid
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_obstacle = False
        self.neighbors = []
        self.parent = None
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.is_open = False
        self.is_closed = False

    def __lt__(self, other):
        return self.f_score < other.f_score

grid = [[Node(row, col) for col in range(NUM_COLS)] for row in range(NUM_ROWS)]
start_node = grid[20][1]
end_node = grid[NUM_ROWS - 3][NUM_COLS - 3]

# Heuristic function (Euclidean distance)
def heuristic(node1, node2):
    return math.sqrt((node1.row - node2.row)**2 + (node1.col - node2.col)**2)

def get_neighbors(node):
    neighbors = []
    row, col = node.row, node.col
    if row > 0:
        neighbors.append(grid[row - 1][col])
    if row < NUM_ROWS - 1:
        neighbors.append(grid[row + 1][col])
    if col > 0:
        neighbors.append(grid[row][col - 1])
    if col < NUM_COLS - 1:
        neighbors.append(grid[row][col + 1])
    return [neighbor for neighbor in neighbors if not neighbor.is_obstacle]

def a_star_algorithm(start, end):
    open_set = []
    heapq.heappush(open_set, start)
    start.g_score = 0
    start.f_score = heuristic(start, end)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node == end:
            # Reconstruct path
            path = []
            node = current_node
            while node:
                path.append(node)
                node = node.parent
            return path[::-1]

        current_node.is_closed = True
        for neighbor in get_neighbors(current_node):
            if neighbor.is_closed:
                continue

            tentative_g_score = current_node.g_score + heuristic(current_node, neighbor)
            if tentative_g_score < neighbor.g_score:
                neighbor.parent = current_node
                neighbor.g_score = tentative_g_score
                neighbor.f_score = neighbor.g_score + heuristic(neighbor, end)
                if not neighbor.is_open:
                    heapq.heappush(open_set, neighbor)
                    neighbor.is_open = True

def draw_start_point():
    pygame.draw.circle(screen, BLUE, (start_node.col * CELL_SIZE + CELL_SIZE // 2, start_node.row * CELL_SIZE + CELL_SIZE // 2), 6)

def draw_end_point():
    pygame.draw.circle(screen, RED, (end_node.col * CELL_SIZE + CELL_SIZE // 2, end_node.row * CELL_SIZE + CELL_SIZE // 2), 6)

def draw_path(path):
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        pygame.draw.line(screen, GREEN, (current_node.col * CELL_SIZE + CELL_SIZE // 2, current_node.row * CELL_SIZE + CELL_SIZE // 2),
                         (next_node.col * CELL_SIZE + CELL_SIZE // 2, next_node.row * CELL_SIZE + CELL_SIZE // 2), 6)
        pygame.display.flip()
        pygame.time.delay(75)

def draw_grid():
    for row in grid:
        for node in row:
            if node.is_obstacle:
                pygame.draw.rect(screen, BLACK, (node.col * CELL_SIZE, node.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (node.col * CELL_SIZE, node.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (node.col * CELL_SIZE, node.row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def reset_grid():
    for row in grid:
        for node in row:
            node.is_open = False
            node.is_closed = False
            node.g_score = float('inf')
            node.f_score = float('inf')
            node.parent = None

def reset():
    global setting_start, setting_end
    reset_grid()
    setting_start = True
    setting_end = False

setting_start = True
setting_end = False
running = True
algorithm_running = False
time_since_completion = 0
delay_duration = 9000
last_clicked_node = None  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not algorithm_running:
            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                row = event.pos[1] // CELL_SIZE

                clicked_node = grid[row][col]

                if event.button == 1:
                    if setting_start:
                        start_node = clicked_node
                        setting_start = False
                        setting_end = True
                    elif setting_end:
                        if clicked_node != start_node:
                            end_node = clicked_node
                            setting_end = False
                            algorithm_running = True

                elif event.button == 3:
                    if clicked_node != start_node and clicked_node != end_node:
                        clicked_node.is_obstacle = not clicked_node.is_obstacle

                last_clicked_node = clicked_node

    draw_grid()

    if not setting_start:
        draw_start_point()
    if not setting_end and algorithm_running:
        draw_end_point()

    if algorithm_running:
        if time_since_completion == 0:
            # Mark the start time of the delay
            time_since_completion = pygame.time.get_ticks()

        # Perform the A* algorithm during the delay
        if pygame.time.get_ticks() - time_since_completion <= delay_duration:
            path = a_star_algorithm(start_node, end_node)

            if path:
                draw_path(path)
                pygame.display.flip()
            continue # Skip the rest of the loop during the delay

        # Reset everything after the delay
        reset()
        algorithm_running = False
        time_since_completion = 0

    pygame.display.flip()

pygame.quit()