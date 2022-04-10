from dataclasses import dataclass
import pygame

# Define o relógio
clock = pygame.time.Clock()

# Inicializa pygame
pygame.init()

# Define a cor de fundo
BACKGROUND_COLOR = (70,86,94)

# Define o nome da janela
pygame.display.set_caption('PyGame')

# Define o número de quadros por segundo
FPS = 60

# Define o tamanho da tela
WIDTH, HEIGHT = 450, 200
WINDOW_SIZE = (WIDTH, HEIGHT)

# Inicia a tela
screen = pygame.display.set_mode(WINDOW_SIZE, True, 32)

# Carrega e altera a imagem do personagem
player_image = pygame.image.load('player.png').convert_alpha()
player = pygame.transform.scale(player_image, (50,75))

moving_right = False 
moving_left = False

@dataclass
class PlayerLocation:
    x: int 
    y: int

player_location = PlayerLocation(x=155, y=310)
velocity = 3.5

# Game Loop
running = True
while running:   
    # Preenche a tela com cinza              
    screen.fill(BACKGROUND_COLOR) 
    # Desenha o player
    screen.blit(player, (player_location.x, player_location.y))

    if moving_right:
        player_location.x += velocity
    if moving_left: 
        player_location.x -= velocity
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True 
            if event.key == pygame.K_LEFT:
                moving_left = True 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False 
            if event.key == pygame.K_LEFT:
                moving_left = False
    
    if player_location.x < 0:
        player_location.x = 0
    elif player_location.x + player.get_width() > WIDTH:
        player_location.x = WIDTH - player.get_width()
    elif player_location.y + player.get_height() > HEIGHT:
        player_location.y = HEIGHT - player.get_height()

    pygame.display.update() 
    clock.tick(FPS) 

pygame.quit()