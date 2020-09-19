import pygame
pygame.init()

def main():
    # Inicializa a Tela
    screen = pygame.display.set_mode((250, 100))
    pygame.display.set_caption('PyGame Text')

    # Define e Preenche o Background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((15, 15, 15))

    # Define, Posiciona e Apresenta o Texto no Background
    font = pygame.font.SysFont('dyuthi', 36)
    text = font.render("Hello PyGame", 1, (195, 195, 195))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    background.blit(text, textpos)

    # Loop de Eventos
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Desenha o Background
        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__': 
    main()