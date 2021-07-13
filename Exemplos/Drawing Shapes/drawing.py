from math import pi
import pygame as pg
pg.init()

# Cores
BLACK = (27, 27, 27)
WHITE = (255, 255, 255)
GREEN = (42, 130, 72)
BLUE = (92, 127, 184)
YELLOW = (199, 177, 36)
RED = (179, 41, 7)

# Define dimensões do display
width = 600
height = 450
screen = pg.display.set_mode([width, height])

# Define três retângulos
retangulos = [
    pg.Rect(20, 20, 100, 50), 
    pg.Rect(20, 90, 50, 50),
    pg.Rect(500, 30, 80, 60)
]

done = True

while done:
    screen.fill(BLACK)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = False
    
    # Desenha três retângulos azuis
    for retangulo in retangulos:
        pg.draw.rect(screen, BLUE, retangulo)

    # Desenha um retângulo verde
    pg.draw.rect(screen, GREEN, [115, 280, 70, 40])
    # Desenha um retângulo vermelho (borda)
    pg.draw.rect(screen, RED, [115, 280, 71, 41], 2)
    # Desenha um círculo amarelo
    pg.draw.circle(screen, YELLOW, (325,70), 30)
    # Desenha um círculo azul
    pg.draw.circle(screen, BLUE, [250, 250], 25, True)
    # Desenha uma elipse branca
    pg.draw.ellipse(screen, WHITE, (250, 300, 100, 100))
    # Desenha um arco vermelho
    pg.draw.arc(screen, RED, [430, 150, 150, 125], pi/100, 1.13*pi, 2)
    # Desenha uma linha azul
    pg.draw.line(screen, BLUE, (0, height-100), (width, height-100), 5)
    # Desenha uma linha verde
    pg.draw.aaline(screen, GREEN, (0, height-200), (width, height-200))
    # Desenha linhas brancas
    pg.draw.lines(screen, WHITE, False, [[400, 400], [400, 20], [200, 20]], 2)
    # Desenha um polígono amarelo
    pg.draw.polygon(screen, YELLOW, [[140, 120], [100, 200], [300, 200]])
    # Desenha um polígono verde (borda)
    pg.draw.polygon(screen, GREEN, [[140, 120], [100, 200], [300, 200]], 3)

    pg.display.update()
    
pg.quit()