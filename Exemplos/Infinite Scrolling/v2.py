import pygame
import math 

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SIZE = (WIDTH, HEIGHT) = 1040, 585
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Infinite Scrolling')

alien_ship = pygame.image.load('alien_ship.png').convert_alpha()
alien_ship_scaled = pygame.transform.scale(alien_ship,(125,85))
background = pygame.image.load('city.png').convert_alpha()
background_width = background.get_width()
background_rect = background.get_rect()

scroll = 0
direction = 0
speed = 2.5
panels = math.ceil(WIDTH / background_width) + 2 

run = True
while run:
    clock.tick(FPS)

    for i in range(panels):
        screen.blit(background, (i * background_width + scroll - background_width, 0))

    screen.blit(alien_ship_scaled,(450,220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = -1
            if event.key == pygame.K_LEFT:
                direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 0

    scroll += speed * direction
    if abs(scroll) > background_width:
        scroll = 0

    pygame.display.flip()

pygame.quit()