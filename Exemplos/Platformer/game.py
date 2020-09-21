from pygame.locals import *
from physics import collision_test, move
import pygame, sys
pygame.init() 

def load_map(file):
    game_map = []
    with open(f'{file}','r') as f:
        data = f.read()
    [game_map.append(list(row)) for row in data.split('\n')]      
    return game_map

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = f'{animation_name}_{str(n)}'
        img_loc = f'{path}/{animation_frame_id}.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_action):
    if action_var != new_action:
        action_var = new_action
        frame = 0
    return action_var,frame

clock = pygame.time.Clock()
pygame.display.set_caption('Platformer')
WINDOW_SIZE = (800,600)
screen = pygame.display.set_mode(WINDOW_SIZE) 
display = pygame.Surface((300,200))
FPS = 60

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
true_scroll = [0,0]

global animation_frames
animation_frames = {}
animation_database = {}
animation_database['run'] = load_animation('player/run',[7,7])
animation_database['idle'] = load_animation('player/idle',[7,7,40])

game_map = load_map('mapa.txt')
grass_img = pygame.image.load('grama.png')
rock_img = pygame.image.load('rocha.png')

player_action = 'idle'
player_frame = 0
player_flip = False
player_rect = pygame.Rect(100,100,23,30)

while True: 
    display.fill((154,166,166)) 
    if player_rect.x < 130:
        true_scroll[0] += (player_rect.x-true_scroll[0]+93)/20
    if player_rect.x > 1750:
        true_scroll[0] += (player_rect.x-true_scroll[0]-363)/20
    if player_rect.y < 3:
        true_scroll[1] += (player_rect.y-true_scroll[1]-56)/20
    true_scroll[0] += (player_rect.x-true_scroll[0]-132)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(rock_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x += 1
        y += 1

    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')

    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),
        (player_rect.x-scroll[0],player_rect.y-scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -4
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(FPS)