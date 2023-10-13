import pygame
import csv

SIZE = (WIDTH, HEIGHT) = 800, 640
ROWS, COLS = 20, 150
TILE_SIZE = HEIGHT // ROWS
TILE_TYPES = 4
screen_scroll = 0 
bg_scroll = 0
SCROLL_THRESH = 200
GRAVITY = 0.75
moving_left = False 
moving_right = False
FPS = 60
SKY = (161, 173, 255)

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Mario 3.0')
clock = pygame.time.Clock()

tile_list = []
for tile in range(TILE_TYPES):
    img = pygame.image.load(f'imagens/tiles/{tile}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_list.append(img)

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_w, scale_h, speed):
        pygame.sprite.Sprite.__init__(self)
        self.raw_image = pygame.image.load('imagens/mario.png').convert_alpha()
        self.image = pygame.transform.scale(self.raw_image, (int(img.get_width() * scale_w), int(img.get_height() * scale_h)))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.flip = False
        self.jump = False
        self.in_air = False
        self.vel_y = 0

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        dx, dy = 0, 0 

        if moving_left:
            dx = -self.speed
            self.flip = True
        if moving_right:
            dx = self.speed
            self.flip = False 
        if self.jump and not self.in_air:
            self.vel_y = -13
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0 
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0 
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom  

        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
            dx = 0  

        self.rect.x += dx 
        self.rect.y += dy 

        if (self.rect.right > WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - WIDTH) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.rect.x -= dx 
            screen_scroll = -dx
        return screen_scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])

        for y,row in enumerate(data):
            for x,tile in enumerate(row):
                if tile == 0: 
                    player = Mario(x * TILE_SIZE, y * TILE_SIZE, 1.25, 1.55, 5)
                elif tile >= 1:
                    img = tile_list[tile-1]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 1 and tile <= 4:
                        self.obstacle_list.append(tile_data)
        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

with open('mapas/mapa.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x,row in enumerate(reader):
        for y,tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player = world.process_data(world_data)

running = True
while running:
    clock.tick(FPS)
    screen.fill(SKY)

    world.draw()
    player.draw()
    screen_scroll = player.move(moving_left, moving_right)
    bg_scroll -= screen_scroll

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True 
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False 
            if event.key == pygame.K_d:
                moving_right = False    
    
    pygame.display.flip()

pygame.quit()