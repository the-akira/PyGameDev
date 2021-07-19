from spritesheet import SpriteSheet
import pygame
pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('spritesheet.png').convert_alpha()
sprite_sheet = SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

def get_image(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image

frame_0 = get_image(sprite_sheet_image, 0, 24, 24, 3, BLACK)
frame_1 = get_image(sprite_sheet_image, 1, 24, 24, 3, BLACK)
frame_2 = get_image(sprite_sheet_image, 2, 24, 24, 3, BLACK)
frame_3 = sprite_sheet.get_image(3, 24, 24, 3, BLACK)
frame_4 = sprite_sheet.get_image(4, 24, 24, 3, BLACK)
frame_5 = sprite_sheet.get_image(5, 24, 24, 3, BLACK)

run = True 
while run:
    screen.fill(BG)
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (60, 0))
    screen.blit(frame_2, (120, 0))
    screen.blit(frame_3, (180, 0))
    screen.blit(frame_4, (240, 0))
    screen.blit(frame_5, (300, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()