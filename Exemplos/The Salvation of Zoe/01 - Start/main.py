import pygame

# Inicialize o Pygame
pygame.init()

# Defina as constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60

# Cores
BLACK = (0, 0, 0)

# Crie a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Plataforma 2D")

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpar a tela
    screen.fill(BLACK)

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

# Encerrar o Pygame
pygame.quit()