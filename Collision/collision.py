from pygame.locals import * 
from random import randint
from sys import exit
import pygame
pygame.init()

# Define cores
BLACK = (12, 12, 12)
WHITE = (255, 255, 255)
BLUE = (96, 110, 150)
RED = (255, 0, 0)
 
# Define o width e height da screen [width, height]
width = 500
height = 400
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
 
# Game Loop fica ativo até que jogando seja False
playing = True
clock = pygame.time.Clock()

player_image = pygame.image.load('sprites/player.png').convert_alpha()
player_transformed = pygame.transform.scale(player_image, (70,70))
player_rect = player_transformed.get_rect()

portal_image = pygame.image.load('sprites/portal.png')
portal_transformed = pygame.transform.scale(portal_image, (70,70))
portal_rect = portal_transformed.get_rect()

trunk_image = pygame.image.load('sprites/trunk.png')
trunk_image.set_colorkey(WHITE)
trunk_transformed = pygame.transform.scale(trunk_image, (80,80))
trunk_rect = portal_transformed.get_rect()

# Posição Inicial do player
player_x = 20
player_y = 20

# Velocidade e Direção do player
player_change = 3.5

moving_right = False 
moving_left = False
moving_top = False 
moving_down = False
 
while playing:
    screen.fill(BLUE)

    if moving_right == True:
        player_x += player_change
    if moving_left == True: 
        player_x -= player_change
    if moving_top == True:
        player_y -= player_change
    if moving_down == True: 
        player_y += player_change  

    player_rect.x = player_x
    player_rect.y = player_y
    portal_rect.x = 140
    portal_rect.y = 170
    trunk_rect.x = 300
    trunk_rect.y = 250

    if player_rect.colliderect(portal_rect):
        print('ocorreu uma colisão entre os objetos')
        player_x = randint(35,450)
        player_y = randint(35,350)

    if player_rect.colliderect(trunk_rect):
        print('ocorreu uma colisão entre os objetos')
        exit()

    if player_x < 0:
        player_x = 0
    elif player_x + player_transformed.get_width() > width:
        player_x = width - player_transformed.get_width()
    if player_y < 0:
        player_y = 0
    elif player_y + player_transformed.get_height() > height:
        player_y = height - player_transformed.get_height()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True 
            if event.key == K_LEFT:
                moving_left = True 
            if event.key == K_UP:
                moving_top = True
            if event.key == K_DOWN:
                moving_down = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False 
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_top = False
            if event.key == K_DOWN:
                moving_down = False

    screen.blit(player_transformed, [player_rect.x, player_rect.y])
    screen.blit(portal_transformed, [portal_rect.x, portal_rect.y])
    screen.blit(trunk_transformed, [trunk_rect.x, trunk_rect.y])

    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()