from dataclasses import dataclass
import pygame
pygame.init()

# Define cores
WHITE = (255, 255, 255)
BLACK = (17, 17, 17)
 
# Define o comprimento e altura (WIDTH e HEIGHT) da tela (screen)
WIDTH = 500
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collisions")
 
# Game Loop ficará ativo até que playing seja False
playing = True
# Define relógio e quadros por segundo
clock = pygame.time.Clock()
FPS = 60

# Carrega o fundo
background = pygame.image.load('sprites/background.png').convert_alpha()

# Carrega o sprite, transforma sua dimensão, obtém retângulo e define posição x e y
player_image = pygame.image.load('sprites/player.png').convert_alpha()
player_transformed = pygame.transform.scale(player_image, (50,75))
player_rect = player_transformed.get_rect()
player_rect.x = 10
player_rect.y = 10
# Velocidade x e y do player
dx = 3.5
dy = 3.5

portal_image = pygame.image.load('sprites/portal.png').convert_alpha()
portal_transformed = pygame.transform.scale(portal_image, (65,65))
portal_rect = portal_transformed.get_rect()
portal_rect.x = 195
portal_rect.y = 95

trunk_image = pygame.image.load('sprites/trunk.png')
trunk_image.set_colorkey(WHITE)
trunk_transformed = pygame.transform.scale(trunk_image, (65,65))
trunk_rect = trunk_transformed.get_rect()
trunk_rect.x = 355
trunk_rect.y = 205

box_image = pygame.image.load('sprites/box.png').convert_alpha()
box_transformed = pygame.transform.scale(box_image, (65,65))
box_rect = box_transformed.get_rect()
box_rect.x = 100
box_rect.y = 255

skull_image = pygame.image.load('sprites/skull.png').convert_alpha()
skull_transformed = pygame.transform.scale(skull_image, (60,70))
skull_rect = skull_transformed.get_rect()
skull_rect.x = 430
skull_rect.y = 10

# Direção do personagem
moving_right = False 
moving_left = False
moving_top = False 
moving_down = False

# Movimento e colisões
@dataclass
class Movement:
    x: int 
    y: int

def collision_test(player, obstacles):
    collisions = []
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            collisions.append(obstacle)
    return collisions

def move_and_collide(player, movement, obstacles):
    player.x += movement.x
    collisions_x = collision_test(player, obstacles)
    for obstacle in collisions_x:
        if movement.x > 0:
            player.right = obstacle.left
        if movement.x < 0:
            player.left = obstacle.right
        if obstacle.x == skull_rect.x:
            screen.fill(BLACK)
    player.y += movement.y
    collisions_y = collision_test(player, obstacles)
    for obstacle in collisions_y:
        if movement.y > 0:
            player.bottom = obstacle.top
        if movement.y < 0:
            player.top = obstacle.bottom
        if obstacle.y == skull_rect.y:
            screen.fill(BLACK)

# Início do Game Loop
while playing:
    screen.blit(background, (0,0))

    movement = Movement(x=0, y=0)
    if moving_right:
        movement.x += dx
    if moving_left: 
        movement.x -= dx
    if moving_top:
        movement.y -= dy
    if moving_down: 
        movement.y += dy  

    if player_rect.x < 0:
        player_rect.x = 0
    elif player_rect.x + player_transformed.get_width() > WIDTH:
        player_rect.x = WIDTH - player_transformed.get_width()
    if player_rect.y < 0:
        player_rect.y = 0
    elif player_rect.y + player_transformed.get_height() > HEIGHT:
        player_rect.y = HEIGHT - player_transformed.get_height()

    if player_rect.colliderect(portal_rect):
        player_rect.x = 430
        player_rect.y = 310

    obstacles = [trunk_rect, box_rect, skull_rect]
    move_and_collide(player_rect, movement, obstacles)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True 
            if event.key == pygame.K_LEFT:
                moving_left = True 
            if event.key == pygame.K_UP:
                moving_top = True
            if event.key == pygame.K_DOWN:
                moving_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False 
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_UP:
                moving_top = False
            if event.key == pygame.K_DOWN:
                moving_down = False

    screen.blit(player_transformed, [player_rect.x, player_rect.y])
    screen.blit(portal_transformed, [portal_rect.x, portal_rect.y])
    screen.blit(trunk_transformed, [trunk_rect.x, trunk_rect.y])
    screen.blit(box_transformed, [box_rect.x, box_rect.y])
    screen.blit(skull_transformed, [skull_rect.x, skull_rect.y])

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()