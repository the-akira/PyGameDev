import pygame

# Configurações globais
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
SCREEN_SIZE = pygame.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
INITIAL_POS = (35, 500)  # Posição inicial mais adequada
BACKGROUND_BLUE = (104, 136, 247)
GRAVITY = 0.5
JUMP_STRENGTH = -12  # Valor negativo para ir para cima
PLAYER_SPEED = 5
TILE_SIZE = 32
FPS = 60

class Camera:
    def __init__(self, target, world_width, world_height):
        self.target = target
        self.camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.world_width = world_width
        self.world_height = world_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self):
        x = -self.target.rect.centerx + SCREEN_WIDTH // 2
        y = -self.target.rect.centery + SCREEN_HEIGHT // 2
        
        # Limitar a câmera aos limites do mundo
        x = min(0, x)  # Lado esquerdo
        x = max(-(self.world_width - SCREEN_WIDTH), x)  # Lado direito
        y = min(0, y)  # Topo
        y = max(-(self.world_height - SCREEN_HEIGHT), y)  # Base
        
        self.camera = pygame.Rect(x, y, self.world_width, self.world_height)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, platforms):
        super().__init__()
        self.original_image = pygame.image.load('mario.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (45, 55))
        self.image = self.original_image
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.image.get_rect(topleft=pos)
        
        # Física
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, GRAVITY)
        self.on_ground = False
        self.platforms = platforms
        
        # Movimento
        self.speed = PLAYER_SPEED
        self.jump_strength = JUMP_STRENGTH
        self.running_multiplier = 1.5

    def update(self):
        self.handle_input()
        self.apply_physics()
        self.handle_collisions()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Movimento horizontal
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.image = self.flipped_image
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.image = self.original_image
            
        # Aceleração (corrida)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity.x *= self.running_multiplier
            
        # Pulo
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity.y = self.jump_strength
            self.on_ground = False

    def apply_physics(self):
        # Aplicar gravidade
        if not self.on_ground:
            self.velocity.y += self.acceleration.y
            # Limitar velocidade de queda
            self.velocity.y = min(self.velocity.y, 15)

    def handle_collisions(self):
        # Movimento horizontal
        self.rect.x += self.velocity.x
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.x > 0:  # Movendo para a direita
                    self.rect.right = platform.rect.left
                elif self.velocity.x < 0:  # Movendo para a esquerda
                    self.rect.left = platform.rect.right

        # Movimento vertical
        self.rect.y += self.velocity.y
        self.on_ground = False
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity.y > 0:  # Caindo
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity.y = 0
                elif self.velocity.y < 0:  # Pulando
                    self.rect.top = platform.rect.bottom
                    self.velocity.y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_load = pygame.image.load('brick.png').convert_alpha()
        self.image = pygame.transform.scale(self.image_load, (TILE_SIZE,TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

def create_level(level_layout, platform_group, all_sprites):
    for y, row in enumerate(level_layout):
        for x, tile in enumerate(row):
            if tile == "P":
                Platform((x * TILE_SIZE, y * TILE_SIZE)).add(platform_group, all_sprites)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mario")
    clock = pygame.time.Clock()

    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                      P",
        "P                                                      P",
        "P                                                      P",
        "P                    PPPPPPPPPPP                       P",
        "P                                                      P",
        "P                                            PPPPP     P",
        "P                                                      P",
        "P    PPPPPPPP                                          P",
        "P                                                    PPP",
        "P                          PPPPPPP                     P",
        "P                 PPPP                   PPPPPP        P",
        "P                                                      P",
        "P         PPPP                                         P",
        "P                                                      P",
        "P                     PPPPPP          PPPPPPPPPP       P",
        "P                                                      P",
        "P   PPPPPPPPPPP                                        P",
        "P                                                      P",
        "P                       PPPPPPPP              PPPPPPPPPP",
        "P                                                      P",
        "P             PPPPPP                                   P",
        "P                                                      P",
        "P                                                      P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    ]

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    
    # Criar nível
    level_width = len(level[0]) * TILE_SIZE
    level_height = len(level) * TILE_SIZE
    create_level(level, platforms, all_sprites)
    
    # Criar jogador
    player = Player(INITIAL_POS, platforms)
    all_sprites.add(player)
    
    # Configurar câmera
    camera = Camera(player, level_width, level_height)

    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # Atualizações
        all_sprites.update()
        camera.update()
        
        # Desenho
        screen.fill(BACKGROUND_BLUE)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()