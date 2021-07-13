from pygame import *
import random
 
init()
display.set_caption('Camera Explorer')
screen = display.set_mode((800,600))
sx, sy = screen.get_size()
 
wx, wy = 4000, 4000
worldmap = Surface((wx, wy))
 
worldmap.fill((0, 130, 0))
for _ in range(800):
    c = random.randint(50,140)
    x = random.randint(0, wx)
    y = random.randint(0, wy)
    r = random.randint(wx // 25, wx // 20)
    draw.circle(worldmap, (0, c, 0), (x, y), r)

player_image = image.load('knight.png').convert_alpha()
player_scaled = transform.scale(player_image, (95,95))
 
playing = True
px, py = wx // 2, wy // 2
clock = time.Clock()
f = font.SysFont('dyuthi', 30)

while playing:
    dt = 0.001 * clock.tick()
    k = key.get_pressed()

    for e in event.get():
        if e.type == QUIT:
            playing = False
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            playing = False
 
    # Posição do player em coordenadas do mundo
    px += (k[K_RIGHT] - k[K_LEFT]) * 1000 * dt
    py += (k[K_DOWN] - k[K_UP]) * 1000 * dt
    px = min(max(px, 0), wx)
    py = min(max(py, 0), wy)
 
    # Posição da Câmera (centro da tela em coordenadas do mundo)
    cx = min(max(px, sx//2), wx-sx//2)
    cy = min(max(py, sy//2), wy-sy//2)

    if px < 0:
        px = 0
    elif px + player_scaled.get_width() > wx:
        px = wx - player_scaled.get_width()
    if py < 0:
        py = 0
    elif py + player_scaled.get_height() > wy:
        py = wy - player_scaled.get_height()
 
    # Desenha o mapa do mundo
    screen.blit(worldmap, (sx//2 - cx, sy//2 - cy))
    # Desenha o player
    screen.blit(player_scaled, (int(sx//2 + px - cx), int(sy//2 + py - cy)))
    # Contador de FPS
    screen.blit(f.render("%.1ffps" % clock.get_fps(), True, (255, 255, 255)), (0, 0))
    display.flip()
 
quit()