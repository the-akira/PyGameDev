from physics import collision_test, move
from dataclasses import dataclass
import pygame, sys
pygame.init()

@dataclass
class PlayerMovement:
    x: int = 0
    y: int = 0

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x += (x - self.x - 132) / 20
        self.y += (y - self.y - 106) / 20

    def clamp(self, min_x, max_x, min_y, max_y):
        self.x = max(min_x, min(self.x, max_x))
        self.y = max(min_y, min(self.y, max_y))

def load_map(file):
    game_map = []
    with open(f'{file}', 'r') as f:
        data = f.read()
    [game_map.append(list(row)) for row in data.split('\n')]
    return game_map

def load_animation(path, frame_durations):
    animation_frames = {}
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = f'{animation_name}_{str(n)}'
        img_loc = f'{path}/{animation_frame_id}.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for _ in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data, animation_frames

def change_action(action_var, frame, new_action):
    if action_var != new_action:
        action_var = new_action
        frame = 0
    return action_var, frame

def update_camera(camera, target_rect, map_width, map_height, display_width, display_height):
    camera.update(target_rect.x, target_rect.y)
    camera.clamp(0, map_width - display_width, 0, map_height - display_height)
    return camera

clock = pygame.time.Clock()
pygame.display.set_caption('Platformer')
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((300, 200))
FPS = 60

vertical_momentum = 0
air_timer = 0
true_scroll = Vector2(0, 0)

animation_database = {}
animation_database['run'], animation_frames_run = load_animation('player/run', [7, 7])
animation_database['idle'], animation_frames_idle = load_animation('player/idle', [7, 7, 40])
animation_frames = {**animation_frames_run, **animation_frames_idle}

game_map = load_map('mapa.txt')
grass_img = pygame.image.load('tiles/grama.png')
rock_img = pygame.image.load('tiles/rocha.png')

player_action = 'idle'
player_frame = 0
player_flip = False
player_rect = pygame.Rect(100, 100, 23, 30)
TILE_SIZE = 16
BACKGROUND_COLOR = (154, 166, 166)

map_width = len(game_map[0]) * TILE_SIZE
map_height = len(game_map) * TILE_SIZE

while True:
    display.fill(BACKGROUND_COLOR)

    true_scroll = update_camera(true_scroll, player_rect, map_width, map_height, display.get_width(), display.get_height())
    scroll = Vector2(int(true_scroll.x), int(true_scroll.y))

    tile_rects = []
    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile == '1':
                display.blit(rock_img, (x * TILE_SIZE - scroll.x, y * TILE_SIZE - scroll.y))
            if tile == '2':
                display.blit(grass_img, (x * TILE_SIZE - scroll.x, y * TILE_SIZE - scroll.y))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    player_movement = PlayerMovement()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_movement.x += 2
    if keys[pygame.K_LEFT]:
        player_movement.x -= 2
    if keys[pygame.K_SPACE]:
        if air_timer < 6:
            vertical_momentum = -4

    player_movement.y += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement.x == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    else:
        player_flip = player_movement.x < 0
        player_action, player_frame = change_action(player_action, player_frame, 'run')

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False),
                 (player_rect.x - scroll.x, player_rect.y - scroll.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(FPS)