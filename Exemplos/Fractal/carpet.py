import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Sierpiński Carpet')
screen.fill((255, 255, 255))

def draw_carpet(x, y, size, depth):
    if depth == 0:
        return
    pygame.draw.rect(screen, (0, 0, 0), (x + size / 3, y + size / 3, size / 3, size / 3))
    new_size = size / 3
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            draw_carpet(x + i * new_size, y + j * new_size, new_size, depth - 1)

draw_carpet(0, 0, 800, 8)
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()