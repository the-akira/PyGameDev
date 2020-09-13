import pygame as pg
pg.init()

BACKGROUND = pg.Color('grey54')
DARKBLUE = pg.Color(11, 2, 65)

display = pg.display.set_mode((800,600))
width, height = display.get_size()
clock = pg.time.Clock()

player_image = pg.Surface((30, 60))
player_image.fill(DARKBLUE)
player_size = player_image.get_size()

x = width * 0.45
y = height * 0.25
x_change = 0
y_change = 0
on_ground = False

# Um valor constante que adicionamos à y_change a cada frame
GRAVITY = 0.03

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                x_change = -5
            elif event.key == pg.K_d:
                x_change = 5
            elif event.key == pg.K_w:
                if on_ground: # Pula apenas se o jogador estiver no chão 
                    y_change = -4
                    on_ground = False
        elif event.type == pg.KEYUP:
            if event.key == pg.K_a and x_change < 0:
                x_change = 0
            elif event.key == pg.K_d and x_change > 0:
                x_change = 0

    # Adiciona a constante GRAVITY à variável y_change
    # De forma que o objeto caia mais rápido a cada frame
    y_change += GRAVITY
    x += x_change
    y += y_change

    # Define os limites do jogador
    if x < 0:
    	x = 0
    elif x + player_size[0] > width:
    	x = width - player_size[0]
    if y < 0:
    	y = 0
    elif y + player_size[1] > height:
    	y = height - player_size[1]

    # Pára o objeto quando ele estiver no chão
    if y >= height - 160:
        y = height - 160
        y_change = 0
        on_ground = True

    # Desenha tudo
    display.fill(BACKGROUND)
    pg.draw.line(display, (0, 0, 0), (0, height-100), (width, height-100), 3)
    display.blit(player_image, (x, y))
    pg.display.update()
    clock.tick(60)

pg.quit()