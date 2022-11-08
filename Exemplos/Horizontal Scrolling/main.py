import pygame

pygame.init()
clock = pygame.time.Clock()
FPS = 60

SIZE = (WIDTH, HEIGHT) = 600, 410
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Horizontal Scrolling')

background = pygame.image.load('map.png').convert_alpha()
starting_pos = 0
ending_pos = 2300

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    starting_pos -= 2

    total = starting_pos

    if total < ending_pos * -1:
        total = ending_pos

    screen.blit(background, (total, 0))

    pygame.display.flip()

pygame.quit()