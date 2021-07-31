import sys, pygame
pygame.init()

WIDTH = 800 
HEIGHT = 600
CENTER_X = WIDTH / 2 
CENTER_Y = HEIGHT / 2
max_iteration = 90
scale = 11.0 / (HEIGHT * 430.0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fractal')

def iteration(c):
    i = 0
    z = 0
    mag = 0.0
    while mag < 4.0 and i < max_iteration:
        z = z**2 + c
        mag = z.imag*z.imag + z.real*z.real
        i += 1
    return i

def set_color(i):
    if i == max_iteration:
        col = (0,0,0)
        return col
    else:
        c = (i * 11.3)
        g = 255
        b = 60
        r = 255 - c
        if r < 0:
            r = 0
            g = 255 * 2 - c
            if g < 0:
                g = 0
                b = 255 * 3 - c
                if b < 0:
                    r = g = b = 0
        return(r, g, b)

def draw_field(screen):
    j = 0 + 1j
    for screen_x in range(WIDTH):
        for screen_y in range(HEIGHT):
            x = (screen_x - CENTER_X) * scale - 0.007
            y = (screen_y - CENTER_Y) * scale - 0.755
            c = x + y * j
            iter_value = iteration(c)
            col = set_color(iter_value)
            pygame.draw.line(screen, col, (screen_x, screen_y), (screen_x, screen_y))

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    draw_field(screen)
    pygame.display.update()