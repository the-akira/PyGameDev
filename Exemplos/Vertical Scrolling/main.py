import pygame

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SIZE = (WIDTH, HEIGHT) = 800, 600
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Vertical Scrolling')

background = pygame.image.load('map.png').convert_alpha()
starting_pos = -7075

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

    pygame.display.flip()

pygame.quit()