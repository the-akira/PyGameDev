import pygame
import math 

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SIZE = (WIDTH, HEIGHT) = 1040, 585
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Infinite Scrolling')

background = pygame.image.load('city.png').convert_alpha()
background_width = background.get_width()
background_rect = background.get_rect()

scroll = 0
panels = math.ceil(WIDTH / background_width) + 2 

run = True
while run:
    clock.tick(FPS)

    for i in range(panels):
        screen.blit(background, (i * background_width + scroll - background_width, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    scroll -= 2.5
    if abs(scroll) > background_width:
        scroll = 0

    pygame.display.flip()

pygame.quit()