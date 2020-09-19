import pygame
pygame.mixer.init()

print(f'init = {pygame.mixer.get_init()}')
print(f'channels = {pygame.mixer.get_num_channels()}')
som = pygame.mixer.Sound('american_crow_spring.ogg')
print(f'length = {som.get_length()}')

while True:
	input('Aperte Enter para tocar o Som')
	som.play()
	print('Tocando o som... CTRL+Z para cancelar')