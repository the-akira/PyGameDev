import pygame
import csv

# Inicialize o Pygame
pygame.init()

# Defina as constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
TILE_SIZE = 32
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crie a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Plataforma 2D")

# Carregue o mapa a partir de um arquivo CSV
def load_map(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        game_map = list(reader)
    return game_map

# Função para desenhar o mapa na tela com deslocamento
def draw_map(game_map):
    for row, tiles in enumerate(game_map):
        for col, tile in enumerate(tiles):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if tile == "0":
                pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE))

# Carregue o mapa a partir de um arquivo CSV
game_map = load_map("map.csv")

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpar a tela
    screen.fill(BLACK)

    # Desenhar o mapa com a câmera aplicada
    draw_map(game_map)

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

# Encerrar o Pygame
pygame.quit()