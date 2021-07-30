import pygame
pygame.init()

# Dados gerais do game
WIDTH = 480 # Largura da tela
HEIGHT = 480 # Altura da tela
TILE_SIZE = 48 # Tamanho de cada tile (cada tile é um quadrado)
FPS = 60 # Frames por segundo

# Define a tela e o relógio
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Exemplo de Tiles")
clock = pygame.time.Clock()

# Define os tipos de tile
GRAMA = 0
FLOR1 = 2
FLOR2 = 3

# Carrega os diferentes tipos de tiles
TILE_SET = {
    GRAMA: pygame.image.load("imagens/grass.png").convert_alpha(),
    FLOR1: pygame.image.load("imagens/flower1.png").convert_alpha(),
    FLOR2: pygame.image.load("imagens/flower2.png").convert_alpha()
}

# Define o mapa do game
TILE_MAP = [
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, FLOR2, GRAMA],
    [GRAMA, FLOR1, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, FLOR2, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, FLOR1, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA],
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, FLOR2, GRAMA, GRAMA],   
    [GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA, GRAMA]
]

# Classe que representa um tile
class Tile(pygame.sprite.Sprite):
    # Construtor da classe Tile
    def __init__(self, tile_img, row, column):
        # Construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self)
        # Transforma o tamanho do tile
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
        # Define a imagem do tile
        self.image = tile_img
        # Detalhes sobre o posicionamento
        self.rect = self.image.get_rect()
        # Posiciona o tile na tela
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row

# Cria um grupo de tiles
tiles = pygame.sprite.Group()
# Cria tiles de acordo com o mapa e adiciona eles ao grupo
for row in range(len(TILE_MAP)):
    for column in range(len(TILE_MAP[row])):
        tile_type = TILE_MAP[row][column]
        tile = Tile(TILE_SET[tile_type], row, column)
        tiles.add(tile)

# Main Loop do Game
running = True
while running:
    # Ajusta a velocidade do game
    clock.tick(FPS)
    # Desenha os tiles
    tiles.draw(screen)
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Atualiza a tela
    pygame.display.flip()