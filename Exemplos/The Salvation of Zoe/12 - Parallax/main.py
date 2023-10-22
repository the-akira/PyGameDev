import pygame
import csv
import os

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
BLACK = (0, 0, 0)

# Crie a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Plataforma 2D")

tile_images = {
    "2": pygame.image.load("assets/grass.png").convert_alpha(),
    "3": pygame.image.load("assets/rock.png").convert_alpha(),
}

collectables = []
collectable_image = pygame.image.load("assets/crystal.png").convert_alpha()

doors = []
door_image = pygame.image.load("assets/door.png").convert_alpha()

background1_img = pygame.image.load("assets/background1.png").convert_alpha()
background2_img = pygame.image.load("assets/background2.png").convert_alpha()

scroll = 0

bg_images = []
for i in range(1, 3):
  bg_image = pygame.image.load(f"assets/plx-{i}.png").convert_alpha()
  bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

def draw_bg():
  for x in range(5):
    speed = 1
    for i in bg_images:
      screen.blit(i, ((x * bg_width) - scroll * speed, 0))
      speed += 0.35

# Defina as constantes para o temporizador
GAME_TIME = 3333 # Tempo em segundos
FONT_SIZE = 36
FONT_COLOR = WHITE
GAME_OVER_COLOR = RED

# Carregue uma fonte para o temporizador
font = pygame.font.Font(None, FONT_SIZE)

# Variável para rastrear o tempo restante
time_left = GAME_TIME

# Efeitos sonoros
bell_fx = pygame.mixer.Sound('sounds/bell.wav')
bell_fx.set_volume(0.15)

# Dark Music - The Devil | Tarot
music = pygame.mixer.Sound('sounds/music.mp3')
music.set_volume(0.1)
music.play(loops=-1)

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

# Função para carregar um novo mapa
def change_map(new_map_file):
    global game_map, tile_group, collectables, doors
    game_map = load_map(new_map_file)
    tile_group.empty()
    collectables = []
    doors = []

    for row, tiles in enumerate(game_map):
        for col, tile in enumerate(tiles):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if tile in tile_images:
                tile_obj = Tile(tile_images[tile], x, y)
                tile_group.add(tile_obj)
            if tile == "1":
                collectable = Collectable(collectable_image, x, y)
                collectables.append(collectable)
            if tile == "0":
                door = Door(door_image, x, y)
                doors.append(door)
    return game_map

def transition_effect(screen):
    max_radius = int((SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) ** 0.5)
    radius_step = 8 # Aumente para tornar o efeito mais rápido
    for radius in range(0, max_radius + radius_step, radius_step):
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), radius, 0)
        pygame.display.flip()
        pygame.time.delay(3) # Ajuste conforme necessário para a velocidade do efeito

# Classe para representar o jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.moving_right = False
        self.moving_left = False
        self.soul_points = 0
        animation_types = ['Idle', 'Walk']
        for animation in animation_types:
            # Resetar a lista de temporária de imagens
            temp_list = []
            # Contar o número de arquivos no diretório
            num_of_frames = len(os.listdir(f'assets/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'assets/{animation}/{i}.png')
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

    def update_animation(self):
        # Atualizar animação 
        ANIMATION_COOLDOWN = 100
        # Atualizar imagem dependendo do frame atual
        self.image = self.animation_list[self.action][self.frame_index]
        # Checar se passou tempo suficiente desde a última atualização 
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Se a animação acabou, então resetar ela para o início
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # Checar se a nova ação é diferente da anterior
        if new_action != self.action:
            self.action = new_action
            # Atualizar as configurações da animação
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
            self.flip = True
            self.moving_left = True
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 5
            self.flip = False
            self.moving_right = True
        else:
            self.vel_x = 0
            self.moving_right = False
            self.moving_left = False
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -15

        self.vel_y += 1  # Gravidade
        self.rect.x += self.vel_x
        self.collide_with_walls(self.vel_x, 0)
        self.rect.y += self.vel_y
        self.on_ground = False  # Reseta o estado "on_ground"
        self.collide_with_walls(0, self.vel_y)

        for collectable in collectables:
            if pygame.sprite.collide_rect(self, collectable):
                collectables.remove(collectable)
                self.soul_points += 1
                bell_fx.play()

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

# Classe para construção de botões interativos
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action

restart_img = pygame.image.load('menus/restart.png').convert_alpha()
restart_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 50, restart_img)

start_img = pygame.image.load('menus/start.png').convert_alpha()
start_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 - 60, start_img)

exit_img = pygame.image.load('menus/exit.png').convert_alpha()
exit_button = Button(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2, exit_img)

# Classe para representar os tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Tile, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Collectable(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Collectable, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Door(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super(Door, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Carregue o mapa a partir de um arquivo CSV
game_map = load_map("maps/map.csv")
current_map_file = "maps/map.csv" 

# Crie um grupo para os sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
main_menu = True

tile_group = pygame.sprite.Group()

# Variáveis de câmera
camera_x, camera_y = 0, 0

# Carregar os tiles do mapa
def load_tiles_and_items():
    for row, tiles in enumerate(game_map):
        for col, tile in enumerate(tiles):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if tile in tile_images:
                tile_obj = Tile(tile_images[tile], x, y)
                tile_group.add(tile_obj)
            if tile == "1":  # Valor que representa os coletáveis no mapa
                collectable = Collectable(collectable_image, x, y)
                collectables.append(collectable)
            if tile == "0":  # Valor que representa as portas no mapa
                door = Door(door_image, x, y)
                doors.append(door)

load_tiles_and_items()

# Loop principal
running = True
game_over = False
clock = pygame.time.Clock()
while running:
    screen.blit(background1_img,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not game_over:
                main_menu = True
                transition_effect(screen)

    if main_menu and not game_over:
        if exit_button.draw():
            running = False
        if start_button.draw():
            main_menu = False

    if not main_menu and not game_over:
        screen.blit(background2_img,(0,0))
        draw_bg()
        all_sprites.update()

        if not game_over:
            time_left = max(0, time_left - 1)

        if player.soul_points == 20:
            game_over = True
            transition_effect(screen)

        # Atualizar a câmera para seguir o jogador
        camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        camera_y = player.rect.centery - SCREEN_HEIGHT // 2

        # Limitar a câmera às bordas do mapa
        camera_x = max(0, min(camera_x, len(game_map[0]) * TILE_SIZE - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, len(game_map) * TILE_SIZE - SCREEN_HEIGHT))

        # Desenhar o mapa com a câmera aplicada
        draw_map(game_map, camera_x, camera_y)

        for collectable in collectables:
            screen.blit(collectable.image, (collectable.rect.x - camera_x, collectable.rect.y - camera_y))

        for door in doors:
            screen.blit(door.image, (door.rect.x - camera_x, door.rect.y - camera_y))

        # Detectar colisões com portas
        for door in doors:
            if pygame.sprite.collide_rect(player, door):
                # Determinar qual mapa carregar com base na localização da porta
                if current_map_file == "maps/map.csv":
                    current_map_file = "maps/map2.csv"
                elif current_map_file == "maps/map2.csv":
                    current_map_file = "maps/map3.csv"
                # Carregar o novo mapa
                transition_effect(screen)
                change_map(current_map_file)

        # Desenhar o jogador com a câmera aplicada
        player.draw(camera_x, camera_y)
        player.update_animation()

        if player.moving_left or player.moving_right:
            player.update_action(1) # 1 significa 'correndo'
        else:
            player.update_action(0) # 0 significa 'parado'

        if player.moving_left and scroll > 0:
            scroll -= 0.3
        elif player.moving_right and scroll < 3000:
            scroll += 0.3

        # Desenhar o temporizador na tela
        timer_text = font.render(f"Tempo: {time_left} s", True, FONT_COLOR)
        screen.blit(timer_text, (10, 10))

        # Desenhar a pontuação na tela
        score_text = font.render(f"{player.soul_points}", True, FONT_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH - 35, 10))
        
        if time_left == 0:
            game_over = True

    if game_over:
        if restart_button.draw():
            game_over = False
            time_left = GAME_TIME
            player.soul_points = 0
            player.rect.topleft = (100, 100)
            game_map = change_map("maps/map.csv")
            current_map_file = "maps/map.csv"

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

# Encerrar o Pygame
pygame.quit()