import pygame
pygame.init()

PURPLE = (71, 30, 133)
GRAY = (201, 201, 201)
BLACK = (12, 12, 12)
RED = (212, 49, 8)

SIZE = 500, 200
screen = pygame.display.set_mode(SIZE)

def draw_point(text, pos):
	font = pygame.font.SysFont('Purisa', 15, bold=True)
	img = font.render(text, True, BLACK)
	pygame.draw.circle(screen, RED, pos, 6)
	screen.blit(img, pos)

rect = pygame.Rect(110, 57, 250, 80)
pts = ('topleft', 'topright', 'bottomleft', 'bottomright',
        'midtop', 'midright', 'midbottom', 'midleft', 'center')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)
    pygame.draw.rect(screen, PURPLE, rect, 4)

    for pt in pts:
        draw_point(pt, eval('rect.'+pt))

    pygame.display.flip()

pygame.quit()