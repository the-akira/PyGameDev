import pygame
import math

pygame.init()

# set up the window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fractal Wave Simulation")

# set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# set up the initial wave parameters
wave_count = 5
amplitude = 150
initial_frequency = 0.0001
phase_shift = 0
y_offset = HEIGHT // 2

# define the wave function
def wave(x, frequency):
    y = 0
    for i in range(wave_count):
        y = amplitude * math.sin(5 * math.pi * (i + 1) * frequency * x + phase_shift)
    return y

# set up the game loop
clock = pygame.time.Clock()
running = True
frequency = initial_frequency

while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear the screen
    window.fill(BLACK)

    # draw the wave
    points = []
    for x in range(0, WIDTH):
        y = wave(x, frequency) + y_offset
        points.append((x, y))
    pygame.draw.lines(window, GREEN, False, points, 2)

    # update the wave parameters
    frequency *= 1.01
    phase_shift += 0.1

    # reset the frequency if it gets too high
    if frequency > 0.2:
        frequency = initial_frequency

    # update the display
    pygame.display.update()

    # limit the frame rate
    clock.tick(60)

# clean up
pygame.quit()