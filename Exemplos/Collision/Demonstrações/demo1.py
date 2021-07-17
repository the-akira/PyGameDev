import pygame

pygame.init()
window = pygame.display.set_mode((250, 250))
pygame.display.set_caption('Colisão')
rect = pygame.Rect(*window.get_rect().center, 0, 0).inflate(100, 100)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    point = pygame.mouse.get_pos()
    collide = rect.collidepoint(point)
    color = (255, 0, 0) if collide else (255, 255, 255)

    window.fill(0)
    pygame.draw.rect(window, color, rect)
    pygame.display.flip()

pygame.quit()