import pygame
import csv

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 832
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Board Game")

# Define block size and number of blocks on the screen
block_size = 64
mini_block_size = 16
blocks_on_screen_x = screen_width // block_size
blocks_on_screen_y = screen_height // block_size
mini_blocks_on_screen_x = screen_width // mini_block_size
mini_blocks_on_screen_y = screen_height // mini_block_size
off_set_x = 175
off_set_y = 70
current_state = "map1"

# Function that loads the initial map
def load_map(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        map_data = [[int(value) for value in row] for row in csv_reader]
    return map_data

# Function to load a new map and update player position
def load_new_map(filename, player_start_x, player_start_y, new_state):
    global map_data, map_width, map_height, player_x, player_y, current_state
    map_data = load_map(filename)
    map_width = len(map_data[0])
    map_height = len(map_data)
    player_x = player_start_x
    player_y = player_start_y
    current_state = new_state

# Load the initial map
map_data = load_map("maps/map.csv")

# Calculate the total number of blocks in the map
map_width = len(map_data[0])
map_height = len(map_data)

# Load images
tree = pygame.image.load("images/tree.png")
grass = pygame.image.load("images/grass.png")
dirty = pygame.image.load("images/dirty.png")
knight = pygame.image.load("images/knight.png")

tile_type = {
    "grass": 0,
    "dirty": 1,
    "tree": 2
}

# Initialize player position
player_x = 1
player_y = 1

# Initialize camera position
camera_x = 0
camera_y = 0

# Game loop
running = True
clock = pygame.time.Clock()
movement_delay = 250  # milliseconds
last_movement_time = pygame.time.get_ticks()
show_full_map = False  # Track whether the full map is currently shown
FPS = 60

while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                show_full_map = not show_full_map  # Toggle the full map display

    # Player movement
    if not show_full_map:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - last_movement_time >= movement_delay:
            if keys[pygame.K_LEFT]:
                if player_x > 0 and map_data[player_y][player_x - 1] != tile_type["tree"]:
                    player_x -= 1
                    last_movement_time = current_time
            if keys[pygame.K_RIGHT]:
                if player_x < map_width - 1 and map_data[player_y][player_x + 1] != tile_type["tree"]:
                    player_x += 1
                    last_movement_time = current_time
            if keys[pygame.K_UP]:
                if player_y > 0 and map_data[player_y - 1][player_x] != tile_type["tree"]:
                    player_y -= 1
                    last_movement_time = current_time
            if keys[pygame.K_DOWN]:
                if player_y < map_height - 1 and map_data[player_y + 1][player_x] != tile_type["tree"]:
                    player_y += 1
                    last_movement_time = current_time

    # Check for tile collision
    if current_state == "map1" and map_data[player_y][player_x] == tile_type["dirty"]:
        load_new_map("maps/map2.csv", player_x, player_y, "map2")
    elif current_state == "map2" and map_data[player_y][player_x] == tile_type["dirty"]:
        load_new_map("maps/map3.csv", player_x, player_y, "map3")

    # Update camera position based on player's position
    camera_x = max(0, min(player_x - blocks_on_screen_x // 2, map_width - blocks_on_screen_x))
    camera_y = max(0, min(player_y - blocks_on_screen_y // 2, map_height - blocks_on_screen_y))
    mini_camera_x = max(0, min(player_x - mini_blocks_on_screen_x // 2, map_width - mini_blocks_on_screen_x))
    mini_camera_y = max(0, min(player_y - mini_blocks_on_screen_y // 2, map_height - mini_blocks_on_screen_y))

    # Draw the tiles
    for y in range(camera_y, camera_y + blocks_on_screen_y):
        for x in range(camera_x, camera_x + blocks_on_screen_x):
            if y < map_height and x < map_width:
                block = map_data[y][x]
                if block == tile_type["grass"]:
                    screen.blit(grass, ((x - camera_x) * block_size, (y - camera_y) * block_size))
                if block == tile_type["dirty"]:
                    screen.blit(dirty, ((x - camera_x) * block_size, (y - camera_y) * block_size))
                if block == tile_type["tree"]:
                    screen.blit(tree, ((x - camera_x) * block_size, (y - camera_y) * block_size))

    # Draw the player
    screen.blit(knight, ((player_x - camera_x) * block_size, (player_y - camera_y) * block_size))

    # Draw the full map if it is currently shown
    if show_full_map:
        screen.fill((77, 57, 32))
        for y in range(map_height):
            for x in range(map_width):
                block = map_data[y][x]
                tile_rect = pygame.Rect(
                    (x - mini_camera_x) * mini_block_size + off_set_x, 
                    (y - mini_camera_y) * mini_block_size + off_set_y, 
                    mini_block_size, 
                    mini_block_size
                )
                if block == tile_type["grass"]:
                    pygame.draw.rect(screen, (0, 255, 0), tile_rect)
                if block == tile_type["dirty"]:
                    pygame.draw.rect(screen, (255, 255, 0), tile_rect)
                if block == tile_type["tree"]:
                    pygame.draw.rect(screen, (4, 94, 23), tile_rect)
        player_rect = pygame.Rect(
            (player_x - mini_camera_x) * mini_block_size + off_set_x, 
            (player_y - mini_camera_y) * mini_block_size + off_set_y,
             mini_block_size, 
             mini_block_size
            )
        pygame.draw.rect(screen, (128, 128, 128), player_rect)

    pygame.display.flip()

# Quit the game
pygame.quit()