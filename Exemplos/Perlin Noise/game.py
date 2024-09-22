import pygame
import noise
import numpy as np
import threading

# Configurações do jogo
CHUNK_SIZE = 16  # Tamanho de cada chunk (em blocos)
BLOCK_SIZE = 32  # Tamanho de cada bloco (pixels)
WIDTH, HEIGHT = 640, 480  # Tamanho da janela
SEED = 0  # Semente para o Perlin Noise

# Configurações do Perlin Noise
SCALE = 50.0  # Controla o zoom do Perlin Noise
OCTAVES = 4
PERSISTENCE = 0.5
LACUNARITY = 2.0

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mundo Infinito com Perlin Noise")
clock = pygame.time.Clock()

# Classe para o jogador
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.color = (255, 0, 0)  # Cor do jogador (vermelho)
        self.size = 20  # Tamanho do jogador
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, 
                         (WIDTH // 2 - self.size // 2, 
                          HEIGHT // 2 - self.size // 2, 
                          self.size, self.size))

# Função para gerar um chunk usando Perlin Noise
def generate_chunk(chunk_x, chunk_y):
    chunk_data = np.zeros((CHUNK_SIZE, CHUNK_SIZE))

    for i in range(CHUNK_SIZE):
        for j in range(CHUNK_SIZE):
            global_x = chunk_x * CHUNK_SIZE + i
            global_y = chunk_y * CHUNK_SIZE + j
            
            height = noise.pnoise2(global_x / SCALE, global_y / SCALE,
                                   octaves=OCTAVES, persistence=PERSISTENCE,
                                   lacunarity=LACUNARITY, base=SEED)
            height_normalized = int((height + 0.5) * 255)
            height_normalized = max(0, min(255, height_normalized))
            chunk_data[j][i] = height_normalized
    
    return chunk_data

# Função para desenhar um chunk na tela
def draw_chunk(chunk_data, chunk_x, chunk_y, player):
    for i in range(CHUNK_SIZE):
        for j in range(CHUNK_SIZE):
            value = chunk_data[j][i]
            color = (0, int(value), 0)  # Verde baseado na altura
            screen_x = (chunk_x * CHUNK_SIZE + i) * BLOCK_SIZE - player.x + WIDTH // 2
            screen_y = (chunk_y * CHUNK_SIZE + j) * BLOCK_SIZE - player.y + HEIGHT // 2
            pygame.draw.rect(screen, color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE))

# Criar um lock para garantir que operações de leitura/escrita no dicionário sejam seguras
lock = threading.Lock()

# Função para gerar um chunk em uma thread separada
def generate_chunk_thread(chunk_x, chunk_y, loaded_chunks):
    chunk_data = generate_chunk(chunk_x, chunk_y)
    
    with lock:  # Usar lock para modificar o dicionário com segurança
        loaded_chunks[(chunk_x, chunk_y)] = chunk_data

# Função para carregar os chunks próximos ao jogador e descarregar os distantes
def load_chunks(player, loaded_chunks):
    player_chunk_x = player.x // (CHUNK_SIZE * BLOCK_SIZE)
    player_chunk_y = player.y // (CHUNK_SIZE * BLOCK_SIZE)

    # Chunks que devem ser mantidos (raio de 3x3 ao redor do jogador)
    chunks_to_keep = set()

    for dx in range(-3, 4):
        for dy in range(-3, 4):
            chunk_x = player_chunk_x + dx
            chunk_y = player_chunk_y + dy
            chunks_to_keep.add((chunk_x, chunk_y))

            # Se o chunk ainda não foi gerado, gera-o em uma thread separada
            if (chunk_x, chunk_y) not in loaded_chunks:
                threading.Thread(target=generate_chunk_thread, args=(chunk_x, chunk_y, loaded_chunks)).start()

    # Remove chunks fora do alcance de 3x3
    with lock:  # Usar lock para remover chunks com segurança
        chunks_to_remove = [key for key in loaded_chunks if key not in chunks_to_keep]
        for chunk in chunks_to_remove:
            del loaded_chunks[chunk]

# Configurações iniciais
player = Player(WIDTH // 2, HEIGHT // 2)
loaded_chunks = {}

# Loop principal do jogo
running = True
while running:
    screen.fill((135, 206, 235))  # Cor do céu
    
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    player.move(dx, dy)
    
    # Carregar e desenhar chunks
    load_chunks(player, loaded_chunks)
    
    with lock:  # Usar lock para garantir que o dicionário não mude enquanto desenha
        for (chunk_x, chunk_y), chunk_data in loaded_chunks.items():
            draw_chunk(chunk_data, chunk_x, chunk_y, player)
    
    # Desenhar o jogador
    player.draw()
    
    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)  # Limitar FPS a 60

pygame.quit()