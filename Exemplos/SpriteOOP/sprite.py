import pygame 
import random 
import os

WIDTH = 800
HEIGHT = 600
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# setup assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_folder, 'guy.png')).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH / 2, HEIGHT / 2)
		self.y_speed = 10

	def update(self):
		self.rect.x += 4
		self.rect.y += self.y_speed
		if self.rect.bottom > HEIGHT - 100:
			self.y_speed = -5
		if self.rect.top < 100:
			self.y_speed = 5
		if self.rect.left > WIDTH:
			self.rect.right = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sprite OOP')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True 
while running:
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	all_sprites.update()

	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.flip()

pygame.quit()