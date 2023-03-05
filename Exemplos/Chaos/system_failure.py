import pygame
import numpy as np

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("System Failure")
clock = pygame.time.Clock()

# Wave parameters
freq = 0.01  # base frequency
speed = 0.4  # speed of frequency change
phase = 3  # phase shift of wave
amplitude = 800  # amplitude of wave

# Color palette for the wave
colors = np.zeros((256, 3))
colors[:85, 0] = np.linspace(255, 0, 85)
colors[:85, 1] = np.linspace(0, 255, 85)
colors[85:170, 1] = np.linspace(255, 0, 85)
colors[85:170, 2] = np.linspace(0, 255, 85)
colors[170:, 2] = np.linspace(255, 0, 86)
colors[170:, 0] = np.linspace(0, 255, 86)

# Pygame surface for drawing the wave
surface = pygame.Surface((500, 500))

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update wave parameters
    freq += speed
    phase += np.pi / 30

    # Generate wave data
    x = np.linspace(0, 7 * np.pi, 500)
    y = np.sin(freq * x + phase) * amplitude + 200
    wave = np.round(y).astype(int)

    # Draw wave on the Pygame surface
    surface.fill((0, 0, 0))
    for i in range(500):
        color = colors[wave[i] % 256]
        pygame.draw.line(surface, color, (i, wave[i]), (i, 500))

    # Scale the surface to the screen
    pygame.transform.scale(surface, (500, 500), screen)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(300)

# Quit Pygame
pygame.quit()