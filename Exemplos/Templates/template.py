from pygame.locals import *
import pygame

# Valores constantes
WIDTH = 500
HEIGHT = 400
FPS = 60

# Cores
BLACK = (13, 13, 13)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Inicializa pygame e cria a janela
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Título do Game")
clock = pygame.time.Clock()

# Game Loop
running = True
while running:
    # Manter o loop rodando na velocidade correta
    clock.tick(FPS)
    # Processar Inputs (Eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Atualizar
    # Desenhar / Renderizar
    screen.fill(BLACK)
    # Depois de desenhar tudo: flipar o display
    pygame.display.flip()

pygame.quit()