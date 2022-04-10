import pygame

BLACK = pygame.Color("black")
BACKGROUND = (170, 238, 187)
YELLOW_GREEN = (194, 252, 32)

# (left, top, width, height)
rect1 = pygame.Rect(100, 50, 100, 100)
rect2 = pygame.Rect(100, 50, 102, 102)

pygame.init()
screen = pygame.display.set_mode((310, 310))
pygame.display.set_caption('Retângulo')

running = True
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, YELLOW_GREEN, rect1)
    pygame.draw.rect(screen, BLACK, rect2, 2)
    pygame.display.update()

pygame.quit()