import pygame, csv

BLACK = (0, 0, 0)
SIZE = (WIDTH, HEIGHT) = 480, 288
FPS = 60
LEVELS = 3
TILE_SIZE = 32
OFF_SET = 16
layout, collected = [], []
clock = pygame.time.Clock()

display = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
screen = pygame.Surface(SIZE)
pygame.display.set_caption("Platformer Adventurer")

def load_levels():
    for n in range(0,LEVELS + 1):
        with open(f'levels/level_{n:02d}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            layout.append([])
            for row in reader:
                layout[n].append(''.join([' ' if tile == '-1' else tile for tile in row]))

def init():
    pygame.init()
    pygame.display.init()
    pygame.mixer.init()

def music_on():
    music = pygame.mixer.music.load("sounds/music.wav")
    pygame.mixer.music.set_volume(0.175)
    pygame.mixer.music.play(-1)

init()
load_levels()
music_on()

load = pygame.image.load
player_sprite = load("assets/mage.png").convert_alpha()
tiles_sprite = load("assets/tileset.png").convert_alpha()
diamond = load("assets/tiles/diamond.png").convert_alpha()
background = load("assets/background.png").convert()
title = pygame.transform.scale(load('assets/title.png').convert_alpha(), (WIDTH, HEIGHT))

sfx_magic = pygame.mixer.Sound("sounds/magic.wav")
sfx_crystal = pygame.mixer.Sound("sounds/crystal.wav")

NUM_OF_TILES = tiles_sprite.get_size()[0] // TILE_SIZE
str_num_tiles = [str(x) for x in range(NUM_OF_TILES - 1)]
str_num_tiles = "".join(str_num_tiles)

player_y = 42069
player_x = 42069
room_num = 0
timer = 0
run = True
paused = False
ROWS = len(layout[room_num])
COLUMNS = len(layout[room_num][0])

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.bottom_col = False
        self.top_col = False
        self.left_col = False
        self.right_col = False
        self.frame = 0
        self.face_right = True
        self.timer = 0

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.y_speed < 8:
            self.y_speed += 0.5
        if self.bottom_col:
            self.y_speed = 0
            if self.x_speed > 0:
                self.x_speed -= 0.3
            elif self.x_speed < 0:
                self.x_speed += 0.3
            if abs(self.x_speed) < 0.3:
                self.x_speed = 0

        if self.timer <= 0:
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.bottom_col:
                self.y_speed = -8
            if keys[pygame.K_LEFT] and self.x_speed > -3:
                self.x_speed -= 0.2
                self.face_right = False
            if keys[pygame.K_RIGHT] and self.x_speed < 3:
                self.x_speed += 0.2
                self.face_right = True

        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.frame = timer % 16 < 8
        else:
            self.frame = 0

        if not self.bottom_col and abs(self.y_speed) > 1:
            self.frame = 2
        if self.timer > 0:
            self.frame = (timer % 16 < 8) + 3
            
        self.bottom_col = False
        self.top_col = False
        self.left_col = False
        self.right_col = False
            
    def draw(self):
        screen.blit(
            player_sprite, 
            (int(self.x), int(self.y)),
            (self.frame * TILE_SIZE, (not self.face_right) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

class Diamond:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def update(self):
        if ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5 < TILE_SIZE:
            collected.append((self.x, self.y, room_num))
            player.x_speed = 0
            pygame.mixer.Sound.play(sfx_crystal)
        if (self.x, self.y, self.num) in collected:
            crystal_to_remove.append(self)
   
    def draw(self):
        if not self in crystal_to_remove:
            screen.blit(diamond,(int(self.x), int(self.y)), ((timer % 16 < 6) * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))

class Terrain:
    def __init__(self, x, y, Type):
        self.x = x
        self.y = y
        self.col = False
        self.type = Type

    def update(self):
        if player.x + TILE_SIZE > self.x and player.x < self.x + TILE_SIZE and not self.col:
            if player.y + TILE_SIZE > self.y and player.y + TILE_SIZE < self.y + OFF_SET:
                player.y = self.y - TILE_SIZE
                player.y_speed = 0
                player.bottom_col = True
                self.col = True
                if self.type == 8:
                    player.y -= 15
                    pygame.mixer.Sound.play(sfx_magic)
                elif self.type == 4:
                    player.y_speed = -10
                    player.bottom_col = False
                    pygame.mixer.Sound.play(sfx_magic)
                elif self.type == 5:
                    player.x, player.y = self.x, self.y
                    player.y += 64
                    pygame.mixer.Sound.play(sfx_magic)          
            elif player.y > self.y + OFF_SET and player.y < self.y + TILE_SIZE:
                player.y = self.y + TILE_SIZE
                player.y_speed = 0
                player.top_col = True
                self.col = True

        if player.y + TILE_SIZE > self.y and player.y < self.y + TILE_SIZE and not self.col:
            if player.x + TILE_SIZE > self.x and player.x + TILE_SIZE < self.x + OFF_SET:
                player.x = self.x - TILE_SIZE
                player.x_speed = -0.4
                player.right_col = True
                self.col = True
            elif player.x > self.x + OFF_SET and player.x < self.x + TILE_SIZE:
                player.x = self.x + TILE_SIZE
                player.x_speed = 0.4
                player.left_col = True
                self.col = True

        self.col = False
        
    def draw(self):
        screen.blit(tiles_sprite, (int(self.x), int(self.y)), (self.type * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))

player = Player(0, 0)

while run:
    sprites = []
    crystal_to_remove = []
 
    for i in range(ROWS):
        for j in range(COLUMNS):
            if layout[room_num][i][j] in str_num_tiles:
                val = int(layout[room_num][i][j])
                sprites.append(Terrain(j*TILE_SIZE, i*TILE_SIZE, val))
            elif layout[room_num][i][j] == "9":
                sprites.append(Diamond(j*TILE_SIZE, i*TILE_SIZE, room_num))

    if player not in sprites:
        sprites.append(player)

    if player_y != 42069:
        player.y = player_y
        player.x = player_x
        
    alive = True

    while run and alive:
        timer += 1
        clock.tick(FPS)
        screen.fill(BLACK)

        if room_num == 0 or paused:
            screen.blit(title, (0, 0))
        else:
            screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if room_num == 1 and player.x < 0:
            player.x = 0

        if not room_num == 0 and not paused:
            for entity in sprites:
                entity.update()
                entity.draw()
            for crystal in crystal_to_remove:
                sprites.remove(crystal)
            crystal_to_remove = []

        if player.x + OFF_SET > WIDTH or player.x + OFF_SET < 0:
            alive = False

        keys = pygame.key.get_pressed()
        start_keys = (keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])
        if room_num == 0 and start_keys:
            room_num += 1
            alive = False
        if keys[pygame.K_ESCAPE]:
            paused = True
        if start_keys:
            paused = False
                        
        display.blit(pygame.transform.scale(screen, (WIDTH*2, HEIGHT*2)),(0, 0))
        pygame.display.flip()

        if player.x + OFF_SET < 0:
            player_y = player.y
            player_x = WIDTH - 24
            room_num -= 1
        elif player.x + OFF_SET > WIDTH:
            player_y = player.y
            player_x = -8
            room_num += 1
            
pygame.quit()