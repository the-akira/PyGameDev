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

animation_list = [] # Lista de listas de diferentes animações
animation_steps = [4, 6, 3, 4, 7] # 24 frames no total - 5 ações
action = 0 # Inicia com a ação 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100 # milisegundos
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

run = True 
while run:
    # Preencher o fundo da tela
    screen.fill(BG)   
    # Atualizar animação
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0
    screen.blit(animation_list[action][frame], (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Trocando as animações com UP e DOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and action > 0:
                action -= 1 
                frame = 0
            if event.key == pygame.K_UP and action < len(animation_list) - 1:
                action += 1 
                frame = 0

    pygame.display.update()

pygame.quit()