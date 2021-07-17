import pygame

pygame.init()
window = pygame.display.set_mode((250, 250))
pygame.display.set_caption('Colisão')

sprite1 = pygame.sprite.Sprite()
sprite1.image = pygame.Surface((40, 40))
sprite1.image.fill((255, 0, 0))
sprite1.rect = pygame.Rect(*window.get_rect().center, 0, 0).inflate(40, 40)

sprite2 = pygame.sprite.Sprite()
sprite2.image = pygame.Surface((75, 75))
sprite2.image.fill((0, 255, 0))
sprite2.rect = pygame.Rect(*window.get_rect().center, 0, 0).inflate(75, 75)

all_group = pygame.sprite.Group([sprite2, sprite1])
test_group = pygame.sprite.Group(sprite2)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sprite1.rect.center = pygame.mouse.get_pos()
    collide = pygame.sprite.spritecollide(sprite1, test_group, False)

    window.fill(0)
    all_group.draw(window)
    for s in collide:
        pygame.draw.rect(window, (255, 255, 255), s.rect, 2)
    pygame.display.flip()

pygame.quit()