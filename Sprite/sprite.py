from sys import exit
from pygame.locals import * 
import pygame

# Define o relógio
clock = pygame.time.Clock()

# Inicializa pygame
pygame.init()

# Define o nome da janela
pygame.display.set_caption('PyGame')

# Define o tamanho da tela
WIDTH, HEIGHT = 450, 200
WINDOW_SIZE = (WIDTH, HEIGHT)

# Inicia a tela
screen = pygame.display.set_mode(WINDOW_SIZE, True, 32)

# Carrega a imagem do personagem
player_image = pygame.image.load('player.png').convert_alpha()
player_transformed = pygame.transform.scale(player_image, (50,75))

moving_right = False 
moving_left = False

player_location = [155, 310]
velocity = 3.5

# Game Loop
while True:					
	screen.fill((70,86,94)) # Preenche a tela com cinza
	screen.blit(player_transformed, player_location)

	if moving_right == True:
		player_location[0] += velocity
	if moving_left == True: 
		player_location[0] -= velocity

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				moving_right = True 
			if event.key == K_LEFT:
				moving_left = True 
		if event.type == KEYUP:
			if event.key == K_RIGHT:
				moving_right = False 
			if event.key == K_LEFT:
				moving_left = False
	
	if player_location[0] < 0:
		player_location[0] = 0
	elif player_location[0] + player_transformed.get_width() > WIDTH:
		player_location[0] = WIDTH - player_transformed.get_width()
	elif player_location[1] + player_transformed.get_height() > HEIGHT:
		player_location[1] = HEIGHT - player_transformed.get_height()

	pygame.display.update() # atualiza a tela
	clock.tick(60) # mantém 60 FPS