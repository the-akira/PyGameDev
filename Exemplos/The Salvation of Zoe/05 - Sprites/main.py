import pygame
import csv

# Inicialize o Pygame
pygame.init()

# Defina as constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
TILE_SIZE = 32
FPS = 50

# Cores
WHITE = (255, 255, 255)
BACKGROUND = (39, 42, 54)
RED = (255, 0, 0)

# Crie a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Plataforma 2D")

tile_images = {
    "0": pygame.image.load("assets/grass.png"),
    "1": pygame.image.load("assets/rock.png")
}

# Carregue o mapa a partir de um arquivo CSV
def load_map(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        game_map = list(reader)
    return game_map

# Função para desenhar o mapa na tela com deslocamento
def draw_map(game_map, camera_x, camera_y):
    for row, tiles in enumerate(game_map):
        for col, tile in enumerate(tiles):
            x = col * TILE_SIZE - camera_x
            y = row * TILE_SIZE - camera_y
            if tile in tile_images:
                tile_obj = Tile(tile_images[tile], x, y)
                tile_obj.draw(screen)

# Classe para representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.flip = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
            self.flip = True
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 5
            self.flip = False
        else:
            self.vel_x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15

        self.vel_y += 1  # Gravidade
        self.rect.x += self.vel_x
        self.collide_with_walls(self.vel_x, 0)
        self.rect.y += self.vel_y
        self.on_ground = False  # Reseta o estado "on_ground"
        self.collide_with_walls(0, self.vel_y)

    def collide_with_walls(self, dx, dy):
        for tile in tile_group:
            if pygame.sprite.collide_rect(self, tile):
                if dx > 0:
                    self.rect.right = tile.rect.left
                if dx < 0:
                    self.rect.left = tile.rect.right
                if dy > 0:
                    self.rect.bottom = tile.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                if dy < 0:
                    self.rect.top = tile.rect.bottom
                    self.vel_y = 0

    def draw(self, camera_x, camera_y):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), 
            (self.rect.x - camera_x, self.rect.y - camera_y))

# Classe para representar os tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Tile, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Carregue o mapa a partir de um arquivo CSV
game_map = load_map("map.csv")

# Crie um grupo para os sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

tile_group = pygame.sprite.Group()

# Variáveis de câmera
camera_x, camera_y = 0, 0

# Carregar os tiles do mapa
for row, tiles in enumerate(game_map):
    for col, tile in enumerate(tiles):
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        if tile in tile_images:
            tile_obj = Tile(tile_images[tile], x, y)
            tile_group.add(tile_obj)

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Atualizar a câmera para seguir o jogador
    camera_x = player.rect.centerx - SCREEN_WIDTH // 2
    camera_y = player.rect.centery - SCREEN_HEIGHT // 2

    # Limitar a câmera às bordas do mapa
    camera_x = max(0, min(camera_x, len(game_map[0]) * TILE_SIZE - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, len(game_map) * TILE_SIZE - SCREEN_HEIGHT))

    # Limpar a tela
    screen.fill(BACKGROUND)

    # Desenhar o mapa com a câmera aplicada
    draw_map(game_map, camera_x, camera_y)

    # Desenhar o jogador com a câmera aplicada
    player.draw(camera_x, camera_y)

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

# Encerrar o Pygame
pygame.quit()