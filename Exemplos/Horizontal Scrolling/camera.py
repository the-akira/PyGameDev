import pygame

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SIZE = (WIDTH, HEIGHT) = 600, 410
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Horizontal Scrolling')
MIN_ALTITUDE = 100

CAMERA_BORDERS = {
    'left': 400,
    'right': WIDTH - 400,
    'top': 200,
    'bottom': HEIGHT - 200
}

display_surf = pygame.display.get_surface()
left = CAMERA_BORDERS['left']
top = CAMERA_BORDERS['top']
cam_width = display_surf.get_width() - (CAMERA_BORDERS['left'] * 2)
cam_height = display_surf.get_height() - (CAMERA_BORDERS['top'] * 2)
camera_rect = pygame.Rect(left, top, cam_width, cam_height)

class Helicopter(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('helicopter.png').convert_alpha()
        self.image = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale))
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
        self.last_bomb = pygame.time.get_ticks()

    def update(self, bg_offset_pos):
        speed = 4
        cooldown = 500 

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and -self.rect.x + 480 > -2300:
            self.rect.x += speed
        if key[pygame.K_UP]:
            if self.rect.y < 5: 
                self.rect.y = 5
            self.rect.y -= speed
        if key[pygame.K_DOWN]:
            if self.rect.y > HEIGHT - self.image.get_height() - MIN_ALTITUDE: 
                self.rect.y = HEIGHT - self.image.get_height() - MIN_ALTITUDE
            self.rect.y += speed
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser = Laser(self.rect.centerx + 55 + bg_offset_pos.x, self.rect.top + 40)
            laser_group.add(laser)
            self.last_shot = time_now
        if key[pygame.K_b] and time_now - self.last_bomb > cooldown:
            bomb = Bomb(self.rect.centerx + 20 + bg_offset_pos.x, self.rect.bottom)
            bomb_group.add(bomb)
            self.last_bomb = time_now

    def draw(self, screen, bg_offset_pos):
        screen.blit(self.image, (self.rect.x + bg_offset_pos.x, self.rect.y))

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('laser.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x += 5
        if self.rect.right > WIDTH:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bomb.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 5
        if self.rect.bottom > HEIGHT - MIN_ALTITUDE + 20:
            self.kill()

background = pygame.image.load('map.png').convert_alpha()
starting_pos = 0
ending_pos = 2300

bomb_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
helicopter_group = pygame.sprite.Group()
helicopter = Helicopter(100, HEIGHT - 220, 0.15)
helicopter_group.add(helicopter)

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if helicopter.rect.left < camera_rect.left:
        camera_rect.left = helicopter.rect.left
    if helicopter.rect.right > camera_rect.right:
        camera_rect.right = helicopter.rect.right
    if helicopter.rect.bottom < camera_rect.top:
        camera_rect.top = helicopter.rect.bottom
    if helicopter.rect.bottom > camera_rect.bottom:
        camera_rect.bottom = helicopter.rect.bottom

    offset = pygame.math.Vector2(
        camera_rect.left - CAMERA_BORDERS['left'], 
        camera_rect.top - CAMERA_BORDERS['top']
    )

    if offset.x <= 0:
        offset.x = 0
    elif offset.x >= 2300:
        offset.x = 2300

    if offset.y <= 0:
        offset.y = 0
    elif offset.y >= 410 - HEIGHT:
        offset.y = 410 - HEIGHT

    bg_rect = background.get_rect(topleft=(0,0))
    bg_offset_pos = bg_rect.topleft - offset

    display_surf.blit(background, bg_offset_pos)
    helicopter.update(bg_offset_pos)
    laser_group.update()
    bomb_group.update()
    helicopter.draw(screen, bg_offset_pos)
    laser_group.draw(screen)
    bomb_group.draw(screen)

    pygame.display.flip()

pygame.quit()