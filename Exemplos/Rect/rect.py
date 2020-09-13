import pygame

WIDTH = 500
HEIGHT = 500
FPS = 60

BLACK = pygame.Color("black")
WHITE = (255, 255, 255)

# (left, top, width, height)
rect = pygame.Rect(50, 50, 150, 150)
print('Atributos do Retângulo')
print(dir(rect))
print(f'x={rect.x}, y={rect.y}, width={rect.w}, height={rect.h}')
print(f'left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}')
print(f'topleft={rect.topleft}, topright={rect.topright}')
print(f'bottomleft={rect.bottomleft}, bottomright={rect.bottomright}')
print(f'midleft={rect.midleft}, midright={rect.midright}')
print(f'midtop={rect.midtop}, midbottom={rect.midbottom}')
print(f'center={rect.center}')

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Retângulo')
clock = pygame.time.Clock()

running = True
while running:
	clock.tick(FPS)
	screen.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pygame.draw.rect(screen, WHITE, rect)
	pygame.display.update()

pygame.quit()