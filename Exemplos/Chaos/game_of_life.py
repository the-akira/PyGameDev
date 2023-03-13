import numpy as np
import pygame
import time

pygame.init()

# Set dimensions of the screen
width, height = 810, 810
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption("Game of Life")

# Set background color
BG_COLOR = (25, 25, 25)
screen.fill(BG_COLOR)

# Number of cells
nx_c, ny_c = 50, 50

# Dimensions of each cell
dim_cw = width / nx_c
dim_ch = height / ny_c

# Initial state of the cells
game_state = np.random.choice([0, 1], size=(nx_c, ny_c), p=[0.6, 0.4])

# Add living cells
living_cells = [
    (5, 3), (5, 4), (5, 5),
    (15, 3), (15, 4), (15, 5),
    (21, 21), (22, 22), (22, 23), (21, 23), (20, 23),
    (35, 20), (35, 21), (35, 22), (36, 22)
]

for cell in living_cells:
    game_state[cell[0], cell[1]] = 1

# Run the game loop
while True:
    new_game_state = np.copy(game_state)

    screen.fill(BG_COLOR)
    time.sleep(0.1)

    for y in range(1, nx_c - 1):
        for x in range(1, ny_c - 1):

            # Count the number of living neighbors
            n_neighbors = (
                game_state[(x - 1) % nx_c, (y - 1) % ny_c]
                + game_state[(x) % nx_c, (y - 1) % ny_c]
                + game_state[(x + 1) % nx_c, (y - 1) % ny_c]
                + game_state[(x - 1) % nx_c, (y) % ny_c]
                + game_state[(x + 1) % nx_c, (y) % ny_c]
                + game_state[(x - 1) % nx_c, (y + 1) % ny_c]
                + game_state[(x) % nx_c, (y + 1) % ny_c]
                + game_state[(x + 1) % nx_c, (y + 1) % ny_c]
            )

            # Apply the Game of Life rules
            if game_state[x, y] == 0 and n_neighbors == 3:
                new_game_state[x, y] = 1
            elif game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_game_state[x, y] = 0

            # Draw each cell on the screen
            poly = [
                (x * dim_cw, y * dim_ch),
                ((x + 1) * dim_cw, y * dim_ch),
                ((x + 1) * dim_cw, (y + 1) * dim_ch),
                (x * dim_cw, (y + 1) * dim_ch),
            ]
            if new_game_state[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Update the game state
    game_state = np.copy(new_game_state)

    # Update the screen
    pygame.display.flip()

    # Quit the game if the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)