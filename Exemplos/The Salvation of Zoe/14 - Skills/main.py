import pygame
import random
import time
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

verses = [
    pygame.image.load("verses/Psalm119-105.png").convert_alpha(),
    pygame.image.load("verses/John1-5.png").convert_alpha(),
    pygame.image.load("verses/Matthew5-14.png").convert_alpha(),
    pygame.image.load("verses/Psalm119-130.png").convert_alpha(),
    pygame.image.load("verses/Ephesians5-8.png").convert_alpha(),
    pygame.image.load("verses/Genesis1-3.png").convert_alpha(),
    pygame.image.load("verses/John9-5.png").convert_alpha(),
    pygame.image.load("verses/Isaiah60-1.png").convert_alpha(),
    pygame.image.load("verses/Psalm18-28.png").convert_alpha(),
    pygame.image.load("verses/Daniel2-22.png").convert_alpha(),
    pygame.image.load("verses/Revelation21-23.png").convert_alpha(),
    pygame.image.load("verses/Psalm36-9.png").convert_alpha(),
    pygame.image.load("verses/Ecclesiastes2-13.png").convert_alpha(),
    pygame.image.load("verses/Romans13-12.png").convert_alpha(),
    pygame.image.load("verses/Genesis1-4.png").convert_alpha(),
    pygame.image.load("verses/John12-46.png").convert_alpha(),
    pygame.image.load("verses/Proverbs20-27.png").convert_alpha(),
    pygame.image.load("verses/John1-7.png").convert_alpha(),
]

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
        speed += 0.4

# Defina as constantes para o temporizador
GAME_TIME = 3000 # Tempo
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

teleport_fx = pygame.mixer.Sound('sounds/teleport.wav')
teleport_fx.set_volume(0.15)

dash_fx = pygame.mixer.Sound('sounds/dash.wav')
dash_fx.set_volume(0.15)

mana_fx = pygame.mixer.Sound('sounds/mana.wav')
mana_fx.set_volume(0.15)

portal_fx = pygame.mixer.Sound('sounds/portal.wav')
portal_fx.set_volume(0.065)

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

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = [0, 0]  # Defina a velocidade inicial
        self.color = (0, 0, 0)  # Defina a cor da partícula
        self.lifespan = 60  # Número de quadros que a partícula permanecerá visível

    def update(self):
        # Atualize a posição da partícula com base na velocidade
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifespan -= 1

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
        self.teleport_cooldown = 5  # Defina o tempo de cooldown em segundos
        self.last_teleport_time = 0  # Inicialize o tempo do último teletransporte
        self.dash_cooldown = 2  # Tempo de cooldown em segundos
        self.last_dash_time = 0  # Inicialize o tempo do último "dash"

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

    def teleport(self):
        current_time = time.time()  # Obtenha o tempo atual em segundos
        if current_time - self.last_teleport_time >= self.teleport_cooldown:
            x = random.randint(0, (len(game_map[0]) - 1) * TILE_SIZE)
            y = random.randint(0, (len(game_map) - 1) * TILE_SIZE)
            # Converta as coordenadas em índices de mapa
            map_x = x // TILE_SIZE
            map_y = y // TILE_SIZE
            # Verifique se o local está vazio (não colide com blocos) e se as coordenadas estão dentro dos limites do mapa
            if 0 <= map_x < len(game_map[0]) and 0 <= map_y < len(game_map) and game_map[map_y][map_x] == '2':
                self.rect.topleft = (x, y)
                teleport_fx.play()
                global time_left 
                time_left -= 100
                self.last_teleport_time = current_time  # Atualize o tempo do último teletransporte

    def update_action(self, new_action):
        # Checar se a nova ação é diferente da anterior
        if new_action != self.action:
            self.action = new_action
            # Atualizar as configurações da animação
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def dash(self):
        current_time = time.time()  # Obtenha o tempo atual em segundos
        if current_time - self.last_dash_time >= self.dash_cooldown:
            dash_speed = 120  # Ajuste a velocidade do dash conforme necessário
            new_x = self.rect.x

            if 160 <= self.rect.x <= 1370:
                if self.flip:
                    new_x -= dash_speed
                else:
                    new_x += dash_speed

                # Verifique se o novo X está dentro dos limites do mapa
                self.rect.x = new_x
                dash_fx.play()
                for _ in range(100):  # Gere 10 partículas a cada uso do "dash"
                    particle = Particle(player.rect.centerx, player.rect.centery)  # Use a posição do jogador como ponto de partida
                    particle.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]  # Velocidade aleatória
                    particles.append(particle)
                self.last_dash_time = current_time
            else:
                mana_fx.play() 

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
        if keys[pygame.K_t]:
            self.teleport()
        if keys[pygame.K_d]:
            self.dash()

        if self.rect.y > 1200:
            self.rect.topleft = (100,100)

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
                global time_left 
                time_left += 100
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
restart_button = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, restart_img)

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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and scroll > 0:
        scroll -= 0.5
    elif keys[pygame.K_RIGHT] and scroll < 3000:
        scroll += 0.5

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
            verse = random.choice(verses)
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
                portal_fx.play()
                change_map(current_map_file)

        # Desenhar o jogador com a câmera aplicada
        player.draw(camera_x, camera_y)
        player.update_animation()

        if player.moving_left or player.moving_right:
            player.update_action(1) # 1 significa 'correndo'
        else:
            player.update_action(0) # 0 significa 'parado'

        # Desenhar o temporizador na tela
        timer_text = font.render(f"Tempo: {time_left} s", True, FONT_COLOR)
        screen.blit(timer_text, (10, 10))

        # Desenhar a pontuação na tela
        score_text = font.render(f"{player.soul_points}", True, FONT_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH - 35, 10))

        for particle in particles:
            particle.update()

        for particle in particles:
            pygame.draw.circle(screen, particle.color, (int(particle.x - camera_x), int(particle.y - camera_y)), 4)

        particles = [particle for particle in particles if particle.lifespan > 0]

        if time_left > 0:
            # Calcule o raio com base no tempo restante
            radius = int(((GAME_TIME - time_left) / GAME_TIME) * min(SCREEN_WIDTH, SCREEN_HEIGHT) / 2)
            # Desenhe o círculo preto
            pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), radius)
        
        if time_left == 0:
            game_over = True
            verse = random.choice(verses)

    if game_over:
        # Desenhar versículo na tela
        screen.blit(verse, (55, 55))
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