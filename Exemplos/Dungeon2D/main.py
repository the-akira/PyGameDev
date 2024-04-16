import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
TILE_SIZE = 32
GRAVITY = 0.5
PLAYER_SPEED = 4.5
JUMP_VELOCITY = -10
FPS = 60
TRANSITION_OFFSET = 30
TILE_TYPES = {"floor":"1", "door":"2"}

# Colors
BLACK = (20, 20, 20)

# Create the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon 2D")

# Function to process and load the map
def read_level_map_from_csv(file_path):
    level_map = []  
    with open(file_path, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            row_values = []
            for value in row:
                if value == '1':
                    row_values.append("1")
                elif value == '0':
                    row_values.append("2")
                elif value == '-1':
                    row_values.append("#")
            level_map.append(''.join(map(str, row_values)))   
    return level_map

class Player(pygame.sprite.Sprite):
    def __init__(self, initial_x, initial_y):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (initial_x, initial_y) # Set initial position
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = False
        self.direction = 1
        self.current_map = "map1"
        self.throw_cooldown = 0

    def update(self, camera_x, camera_y):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity.x = -PLAYER_SPEED
            self.direction = -1
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = PLAYER_SPEED
            self.direction = 1
        else:
            self.velocity.x = 0

        if self.on_ground and keys[pygame.K_SPACE]:
            self.velocity.y = JUMP_VELOCITY
            self.on_ground = False
        elif keys[pygame.K_x]:
            self.throw_sword(camera_x, camera_y)

        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

        self.velocity.y += GRAVITY

        self.rect.x += self.velocity.x
        self.check_collisions('x')

        self.rect.y += self.velocity.y
        self.check_collisions('y')

        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(self.rect.x, MAP_WIDTH - TILE_SIZE)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(self.rect.y, MAP_HEIGHT - TILE_SIZE)

    def check_collisions(self, axis):
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                if tile == TILE_TYPES["floor"]:
                    tile_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(tile_rect):
                        if axis == 'x':
                            if self.velocity.x > 0:
                                self.rect.right = tile_rect.left
                            elif self.velocity.x < 0:
                                self.rect.left = tile_rect.right
                        elif axis == 'y':
                            if self.velocity.y > 0:
                                self.rect.bottom = tile_rect.top
                                self.on_ground = True
                                self.velocity.y = 0
                            elif self.velocity.y < 0:
                                self.rect.top = tile_rect.bottom
                                self.velocity.y = 0
                elif tile == TILE_TYPES["door"] and axis == 'x' and self.current_map == "map1":
                    door_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(door_rect):
                        self.load_map("maps/map2.csv", col_index, row_index)
                        self.current_map = "map2"
                elif tile == TILE_TYPES["door"] and axis == 'x' and self.current_map == "map2":
                    door_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(door_rect):
                        self.load_map("maps/map3.csv", col_index, row_index)
                        self.current_map = "map3"
                elif tile == TILE_TYPES["door"] and axis == 'x' and self.current_map == "map3":
                    door_rect = pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if self.rect.colliderect(door_rect):
                        self.load_map("maps/map1.csv", col_index, row_index)
                        self.current_map = "map1"

    def throw_sword(self, camera_x, camera_y):
        if self.throw_cooldown == 0:
            self.throw_cooldown = 35
            sword = Sword(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            sword_group.add(sword)

    def load_map(self, new_map_file, door_col, door_row):
        global level_map, tiles, MAP_WIDTH, MAP_HEIGHT

        # Save the current player position relative to the door's position
        player_door_offset_x = self.rect.x - door_col * TILE_SIZE
        player_door_offset_y = self.rect.y - door_row * TILE_SIZE

        level_map = read_level_map_from_csv(new_map_file)
        tiles.empty()

        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                if tile == TILE_TYPES["floor"]:
                    tiles.add(Tile(col_index, row_index, "floor"))
                if tile == TILE_TYPES["door"]:
                    tiles.add(Tile(col_index, row_index, "door"))

        MAP_WIDTH = len(level_map[0]) * TILE_SIZE
        MAP_HEIGHT = len(level_map) * TILE_SIZE

        # Calculate the new player position based on the saved offset
        if self.current_map == "map1":
            new_player_x = door_col * TILE_SIZE + player_door_offset_x - TRANSITION_OFFSET
        elif self.current_map == "map2" or self.current_map == "map3":
            new_player_x = door_col * TILE_SIZE + player_door_offset_x
        new_player_y = door_row * TILE_SIZE + player_door_offset_y            

        # If transitioning back to the original map, ensure the player stays within bounds
        new_player_x = max(0, new_player_x)
        new_player_x = min(new_player_x, MAP_WIDTH - TILE_SIZE)
        new_player_y = max(0, new_player_y)
        new_player_y = min(new_player_y, MAP_HEIGHT - TILE_SIZE)

        # Update the player's position
        self.rect.topleft = (new_player_x, new_player_y)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        if tile_type == "floor":
            self.image = pygame.image.load("assets/tile.png").convert_alpha()
        if tile_type == "door":
            self.image = pygame.image.load("assets/portal.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sword.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = 7

    def update(self):
        self.rect.x += (self.direction * self.speed)
        if self.rect.right < 0 or self.rect.left > MAP_WIDTH:  # Alteração aqui para usar a largura do mapa
            self.kill()

    def draw(self, surface, camera_x, camera_y):  # Alteração aqui para adicionar posição da câmera
        if self.direction == 1:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        elif self.direction == -1:
            surface.blit(pygame.transform.rotate(self.image, 180),
                (self.rect.x - camera_x, self.rect.y - camera_y))

# Load the map from a file (sample format)
level_map = read_level_map_from_csv("maps/map1.csv")

# Calculate the map dimensions
MAP_WIDTH = len(level_map[0]) * TILE_SIZE
MAP_HEIGHT = len(level_map) * TILE_SIZE

# Create player object
initial_player_x, initial_player_y = 100, 100
player = Player(initial_player_x, initial_player_y)
sword_group = pygame.sprite.Group()

# Create tile sprites
tiles = pygame.sprite.Group()
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == TILE_TYPES["floor"]:
            tiles.add(Tile(col_index, row_index, "floor"))
        if tile == TILE_TYPES["door"]:
            tiles.add(Tile(col_index, row_index, "door"))

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update camera position to follow the player
    camera_x = max(0, player.rect.x - SCREEN_WIDTH // 2)
    camera_y = max(0, player.rect.y - SCREEN_HEIGHT // 2)
    camera_x = min(camera_x, MAP_WIDTH - SCREEN_WIDTH)
    camera_y = min(camera_y, MAP_HEIGHT - SCREEN_HEIGHT)

    player.update(camera_x, camera_y)

    # Render the level
    screen.fill(BLACK)
    for tile in tiles:
        screen.blit(tile.image, (tile.rect.x - camera_x, tile.rect.y - camera_y))

    # Render the sword
    sword_group.update()
    for sword in sword_group:
        sword.draw(screen, camera_x, camera_y)

    # Check if the sword collides with the tiles
    for tile in tiles:
        for sword in sword_group:
            tile_rect_offset = tile.rect.move(-camera_x, -camera_y)
            sword_rect_offset = sword.rect.move(-camera_x, -camera_y)  # Ajuste da posição da espada
            if tile_rect_offset.colliderect(sword_rect_offset):  # Usando o retângulo ajustado da espada
                sword.kill()

    # Render the player
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()