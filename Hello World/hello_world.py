from sys import exit
import pygame 

pygame.init()

GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Hello World PyGame')
font = pygame.font.SysFont('Purisa', 33, bold=True)
text = font.render('Hello World PyGame', True, BLACK)
text_size = text.get_size()

x, y = 0, 0
x_hat, y_hat = 1, 1
speed = 2

clock = pygame.time.Clock()

while True:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	screen.fill(GRAY)
	
	x += speed * x_hat
	y += speed * y_hat

	if x + text_size[0] > screen.get_width() or x <= 0:
		x_hat *= -1

	if y + text_size[1] > screen.get_height() or y <= 0:
		y_hat *= -1

	screen.blit(text,(x, y))
	pygame.display.update()