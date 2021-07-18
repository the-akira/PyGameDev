from random import randrange
import pygame, sys 

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('img/crosshair.png')
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('sound/laser.wav')
        self.gunshot.set_volume(0.25)
        self.squish = pygame.mixer.Sound('sound/squish.wav')
        self.squish.set_volume(0.3)

    def shoot(self):
        self.gunshot.play()
        if pygame.sprite.spritecollide(crosshair, target_group, True):
            self.squish.play()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):   
        super().__init__()
        self.image = pygame.image.load('img/jack.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

pygame.init()
clock = pygame.time.Clock()

# Tela
WIDTH = 700
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooter')
background = pygame.image.load('img/bg.png')
pygame.mouse.set_visible(False)

# Crosshair
crosshair = Crosshair()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

# Target
target_group = pygame.sprite.Group()
for target in range(20):
    new_target = Target(randrange(0,WIDTH),randrange(0,HEIGHT))
    target_group.add(new_target)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()

    pygame.display.flip()
    screen.blit(background, (0, 0))
    target_group.draw(screen)
    crosshair_group.draw(screen)
    crosshair_group.update()
    clock.tick(60)