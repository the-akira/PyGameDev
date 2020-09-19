from pprint import pprint 
import pygame

fonts = pygame.font.get_fonts()

print(f'Existem {len(fonts)} fonts disponíveis')
pprint(fonts)