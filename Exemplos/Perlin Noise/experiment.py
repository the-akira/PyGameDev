import pygame
import noise
import numpy as np

# Definir dimensões da janela
WIDTH, HEIGHT = 700, 700

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perlin Noise com Pygame")

# Função para gerar mapa de altura usando Perlin Noise
def generate_perlin_noise(width, height, scale, octaves, persistence, lacunarity):
    world = np.zeros((height, width))
    
    for i in range(width):
        for j in range(height):
            # O Perlin Noise é gerado usando as coordenadas (i, j)
            noise_value = noise.pnoise2(i / scale, j / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=width, repeaty=height,
                                        base=0)
            # Normalizar valor do noise para [0, 255]
            world[j][i] = int((noise_value + 0.5) * 255)
    
    return world

# Configurações do Perlin Noise
scale = 100.0  # Aumente/diminua para controlar a "granularidade" do noise
octaves = 6    # Controla o número de camadas de detalhe
persistence = 0.5  # Controla a influência de cada camada de detalhe
lacunarity = 2.0   # Controla a frequência de cada camada de detalhe

# Gera o mapa de alturas
noise_map = generate_perlin_noise(WIDTH, HEIGHT, scale, octaves, persistence, lacunarity)

def map_color(value):
    if value < 80:
        return (0, 0, 255)  # Azul para água
    elif value < 170:
        return (34, 139, 34)  # Verde para grama
    else:
        return (139, 137, 137)  # Cinza para montanha

# Loop principal do Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenhar o mapa de alturas gerado
    for i in range(WIDTH):
        for j in range(HEIGHT):
            value = noise_map[j][i]
            color = map_color(value)
            screen.set_at((i, j), color)
    
    pygame.display.flip()

pygame.quit()