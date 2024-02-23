import pygame
import random
import math
import csv

# Configurações de Tela e Mapa
largura_tela, altura_tela = 800, 600
tamanho_tile = 32

tile_map = {
    "portal": 0,
    "wall": 1,
    "floor": 2,
    "grass": 3,
    "rock": 4
}

creature_map = {
    "skeleton": 0,
    "zombie": 1,
    "orc": 2,
    "goblin": 3,
    "necromancer": 4
}

current_map = "mapas/mapa.csv"
maps = {
    'mapas/mapa.csv': 'mapas/mapa2.csv',
    'mapas/mapa2.csv': 'mapas/mapa3.csv',
    'mapas/mapa3.csv': 'mapas/mapa4.csv'
}

# Cores
BLUE = (0, 0, 148)
PURPLE = (90, 0, 168)

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('RPG com Pygame')

class Weapon:
    def __init__(self):
        self.original_image = pygame.image.load("assets/orb.png").convert_alpha()
        self.angle = 0 
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.fired = False
        self.last_shot = pygame.time.get_ticks()

    def update(self, player, offset_x, offset_y, map_manager):
        shot_cooldown = 300
        fireball = None
        self.rect.center = player.rect.center
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx + offset_x
        y_dist = -(pos[1] - self.rect.centery + offset_y)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))

        if pygame.mouse.get_pressed()[0] and not self.fired and \
           (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            fireball = Fireball(self.rect.centerx, self.rect.centery, self.angle, map_manager)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False
        return fireball

    def draw(self, surface, offset_x, offset_y):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2) - offset_x), 
            self.rect.centery - int(self.image.get_height()/2) - offset_y))

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, map_manager):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load("assets/fireball.png").convert_alpha()
        self.angle = angle 
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        self.dx = math.cos(math.radians(self.angle)) * self.speed
        self.dy = -(math.sin(math.radians(self.angle)) * self.speed)
        self.map_manager = map_manager
        self.damage = 1

    def update(self, offset_x, offset_y, creatures):
        self.rect.x += self.dx 
        self.rect.y += self.dy

        # Verificar colisões com as paredes
        for tile in self.map_manager.todos_sprites:
            if isinstance(tile, Tile) and tile.tipo in [tile_map["wall"], tile_map["rock"]]:
                if self.rect.colliderect(tile.rect):
                    self.kill()

        for creature in creatures:
            if creature.vida_atual > 0 and self.rect.colliderect(creature.rect) and creature.spawn_map == current_map:
                creature.receber_dano(self.damage)
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2) - offset_x), 
            self.rect.centery - int(self.image.get_height()/2) - offset_y))

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo
        if self.tipo == tile_map["portal"]:
            self.image = pygame.image.load('assets/tiles/portal.png').convert_alpha()
        elif self.tipo == tile_map["wall"]:
            self.image = pygame.image.load('assets/tiles/wall.png').convert_alpha()
        elif self.tipo == tile_map["floor"]:
            self.image = pygame.image.load('assets/tiles/floor.png').convert_alpha()
        elif self.tipo == tile_map["grass"]:
            self.image = pygame.image.load('assets/tiles/grass.png').convert_alpha()
        elif self.tipo == tile_map["rock"]:
            self.image = pygame.image.load('assets/tiles/rock.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tamanho_tile, y * tamanho_tile)

class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, player, map_manager, kind, spawn_map):
        super().__init__()
        self.image = pygame.image.load(f'assets/creatures/{kind}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.player = player
        self.map_manager = map_manager
        self.velocidade = self.get_random_velocity()
        self.spawn_map = spawn_map
        self.frame_count = 0
        self.change_speed_frequency = 300
        self.vida_maxima = random.randint(1, 5)
        self.vida_atual = self.vida_maxima 

    def is_in_field_of_view(self):
        distance = math.hypot(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
        return distance < 500  # Ajuste este valor conforme necessário

    def get_random_velocity(self):
        return random.randint(80, 140) + random.randint(-10, 25)

    def update(self, dt):
        # Incrementa a contagem de quadros
        self.frame_count += 1

        # Lógica de mudança de velocidade a cada X quadros
        if self.frame_count % self.change_speed_frequency == 0:
            # Muda a velocidade com uma nova velocidade aleatória
            self.velocidade = self.get_random_velocity()

        # Lógica de movimento da criatura apenas se estiver no campo de visão
        if self.is_in_field_of_view():
            direction_x = 0
            direction_y = 0

            if self.player.rect.x < self.rect.x:
                direction_x = -1
            elif self.player.rect.x > self.rect.x:
                direction_x = 1

            if self.player.rect.y < self.rect.y:
                direction_y = -1
            elif self.player.rect.y > self.rect.y:
                direction_y = 1

            self.rect.x += direction_x * self.velocidade * dt
            self.verificar_colisoes_x(direction_x)
            self.rect.y += direction_y * self.velocidade * dt
            self.verificar_colisoes_y(direction_y)

    def receber_dano(self, dano):
        self.vida_atual -= dano

    def verificar_colisoes_x(self, direction_x):
        for tile in self.map_manager.todos_sprites:
            if isinstance(tile, Tile) and tile.tipo in [tile_map["wall"], tile_map["rock"]]:
                if self.rect.colliderect(tile.rect):
                    if direction_x > 0:
                        self.rect.right = tile.rect.left
                    elif direction_x < 0:
                        self.rect.left = tile.rect.right

    def verificar_colisoes_y(self, direction_y):
        for tile in self.map_manager.todos_sprites:
            if isinstance(tile, Tile) and tile.tipo in [tile_map["wall"], tile_map["rock"]]:
                if self.rect.colliderect(tile.rect):
                    if direction_y > 0:
                        self.rect.bottom = tile.rect.top
                    elif direction_y < 0:
                        self.rect.top = tile.rect.bottom

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x, self.vel_y = 0, 0
        self.velocidade = 250

    def update(self, dt, sprites):
        teclas = pygame.key.get_pressed()
        self.vel_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * self.velocidade
        self.vel_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * self.velocidade

        self.rect.x += self.vel_x * dt
        self.verificar_colisoes_x(sprites)
        self.rect.y += self.vel_y * dt
        self.verificar_colisoes_y(sprites)

    def verificar_colisoes_x(self, sprites):
        for tile in sprites:
            if isinstance(tile, Tile) and tile.tipo in [tile_map["wall"], tile_map["rock"]]:
                if self.rect.colliderect(tile.rect):
                    if self.vel_x > 0:
                        self.rect.right = tile.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = tile.rect.right

    def verificar_colisoes_y(self, sprites):
        for tile in sprites:
            if isinstance(tile, Tile) and tile.tipo in [tile_map["wall"], tile_map["rock"]]:
                if self.rect.colliderect(tile.rect):
                    if self.vel_y > 0:
                        self.rect.bottom = tile.rect.top
                    elif self.vel_y < 0:
                        self.rect.top = tile.rect.bottom

class MapManager:
    def __init__(self, initial_map):
        self.current_map = initial_map
        self.load_map()

    def load_map(self):
        self.map_data = self.load_map_data(self.current_map)
        self.largura_mapa = len(self.map_data[0])
        self.altura_mapa = len(self.map_data)
        self.todos_sprites = pygame.sprite.Group()
        self.portais = pygame.sprite.Group()

        for y in range(self.altura_mapa):
            for x in range(self.largura_mapa):
                tipo = self.map_data[y][x]
                tile = Tile(x, y, tipo)
                self.todos_sprites.add(tile)

                if tipo == tile_map["portal"]:
                    portal = Tile(x, y, tipo)
                    self.portais.add(portal)

    def load_map_data(self, arquivo_csv):
        with open(arquivo_csv, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            mapa = [[int(tipo) for tipo in linha] for linha in leitor_csv]
        return mapa

    def map_transition_effect(self, player):
        fade_surface = pygame.Surface((largura_tela, altura_tela))
        fade_surface.fill(BLUE)
        max_radius = int((largura_tela ** 1.8 + altura_tela ** 1.8) ** 0.5)
        radius_step = 8

        for radius in range(0, max_radius + radius_step, radius_step):
            pygame.draw.circle(fade_surface, PURPLE, (largura_tela // 2, altura_tela // 2), radius, 0)
            tela.blit(fade_surface, (0, 0))

            # Atualizar jogador durante a transição
            dt = clock.tick(60) / 1000.0
            player.update(dt, self.todos_sprites)

            # Verificar colisões durante a transição
            player.verificar_colisoes_x(self.todos_sprites)
            player.verificar_colisoes_y(self.todos_sprites)

            pygame.display.flip()
            pygame.time.delay(1)

    def change_map(self, new_map, player):
        self.current_map = new_map
        self.load_map()
        self.map_transition_effect(player)

def criar_criaturas_a_partir_de_arquivo(arquivo, player, map_manager, spawn_map):
    criaturas = []

    with open(arquivo, 'r') as file:
        linhas = file.readlines()

    for y, linha in enumerate(linhas):
        for x, valor in enumerate(map(int, linha.split(','))):
            x_pos = x * tamanho_tile
            y_pos = y * tamanho_tile
            if valor == creature_map["skeleton"]:
                criatura = Creature(x_pos, y_pos, player, map_manager, "skeleton", spawn_map)
                criaturas.append(criatura)
            if valor == creature_map["zombie"]:
                criatura = Creature(x_pos, y_pos, player, map_manager, "zombie", spawn_map)
                criaturas.append(criatura)
            if valor == creature_map["orc"]:
                criatura = Creature(x_pos, y_pos, player, map_manager, "orc", spawn_map)
                criaturas.append(criatura)
            if valor == creature_map["goblin"]:
                criatura = Creature(x_pos, y_pos, player, map_manager, "goblin", spawn_map)
                criaturas.append(criatura)
            if valor == creature_map["necromancer"]:
                criatura = Creature(x_pos, y_pos, player, map_manager, "necromancer", spawn_map)
                criaturas.append(criatura)

    return criaturas

# Inicialização do jogador e do gerenciador de mapas
player = Player(50, 50)
orb = Weapon()
fireball_group = pygame.sprite.Group()
map_manager = MapManager('mapas/mapa.csv')

# Inicializar as criaturas
criaturas_mapa = criar_criaturas_a_partir_de_arquivo(
    'mapas/mapa_Criaturas.csv', player, map_manager, 'mapas/mapa.csv'
)
criaturas_mapa2 = criar_criaturas_a_partir_de_arquivo(
    'mapas/mapa2_Criaturas.csv', player, map_manager, 'mapas/mapa2.csv'
)
creatures = criaturas_mapa + criaturas_mapa2
creatures_group = pygame.sprite.Group(creatures)

# Loop principal
rodando = True
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualizar jogador
    dt = clock.tick(60) / 1000.0
    player.update(dt, map_manager.todos_sprites)

    # Verificar colisão com portal
    colisoes_portal = pygame.sprite.spritecollide(player, map_manager.portais, False)
    if colisoes_portal and current_map in maps:
        current_map = maps[current_map]
        map_manager.change_map(current_map, player)

    # Lógica da câmera
    offset_x = max(0, min(player.rect.x - largura_tela // 2, map_manager.largura_mapa * tamanho_tile - largura_tela))
    offset_y = max(0, min(player.rect.y - altura_tela // 2, map_manager.altura_mapa * tamanho_tile - altura_tela))

    # Renderização do mapa
    for sprite in map_manager.todos_sprites:
        tela.blit(sprite.image, (sprite.rect.x - offset_x, sprite.rect.y - offset_y))

    # Renderizar o jogador
    tela.blit(player.image, (player.rect.x - offset_x, player.rect.y - offset_y))

    orb.draw(tela, offset_x, offset_y)
    fireball = orb.update(player, offset_x, offset_y, map_manager)
    if fireball:
        fireball_group.add(fireball)

    for fireball in fireball_group:
        fireball.update(offset_x, offset_y, creatures_group)
        fireball.draw(tela)

    # Atualizar e renderizar as criaturas
    for creature in creatures_group:
        if creature.spawn_map == current_map and creature.vida_atual > 0:
            tela.blit(creature.image, (creature.rect.x - offset_x, creature.rect.y - offset_y))
            creature.update(dt)

    pygame.display.flip()

# Finalização do Pygame
pygame.quit()