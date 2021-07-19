from button import Button
import pygame 
pygame.init()

# Definar a janela de apresentação
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Buttons Demo')

# Carregar imagens de botão
start_img = pygame.image.load('images/start_btn.png').convert_alpha()
exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()

# Criar instâncias do botão
start_button = Button(100, 200, start_img, 0.8)
exit_button = Button(450, 200, exit_img, 0.8)

# Game Loop
run = True
while run:
    # Pinta o fundo da tela
    screen.fill((202, 228, 241))
    # Desenha os botões
    if start_button.draw(screen):
        print('START!')
    if exit_button.draw(screen):
        print('EXIT!')
    # Lidar com eventos
    for event in pygame.event.get():
        # Sai do game
        if event.type == pygame.QUIT:
            run = False
    # Atualizar a tela
    pygame.display.update()

pygame.quit()