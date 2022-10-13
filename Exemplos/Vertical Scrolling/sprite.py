import pygame

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('spaceship.png').convert_alpha()
        self.image = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale))
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8
        cooldown = 500 

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed
        if key[pygame.K_UP]:
            if self.rect.y < 0: 
                self.rect.y = 0
            self.rect.y -= speed
        if key[pygame.K_DOWN]:
            if self.rect.y > HEIGHT - self.image.get_height(): 
                self.rect.y = HEIGHT - self.image.get_height()
            self.rect.y += speed
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser = Laser(self.rect.centerx, self.rect.top)
            laser_group.add(laser)
            self.last_shot = time_now

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('laser.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SIZE = (WIDTH, HEIGHT) = 800, 600
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Vertical Scrolling')

background = pygame.image.load('map.png').convert_alpha()
starting_pos = -7075

laser_group = pygame.sprite.Group()
spaceship_group = pygame.sprite.Group()
spaceship = SpaceShip(int(WIDTH / 2), HEIGHT - 135, 0.85)
spaceship_group.add(spaceship)

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    starting_pos += 2

    total = starting_pos

    if total > starting_pos * -1:
        total = 0

    screen.blit(background, (0, total))
    spaceship.update()
    laser_group.update()
    spaceship_group.draw(screen)
    laser_group.draw(screen)

    pygame.display.flip()

pygame.quit()