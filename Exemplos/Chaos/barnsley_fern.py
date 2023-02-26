import pygame
import random

pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chaos Game - Barnsley Fern")
delay_time = 15

# Define the functions for the Barnsley fern
def f1(x, y):
    return 0, 0.16 * y

def f2(x, y):
    return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6

def f3(x, y):
    return 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6

def f4(x, y):
    return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

# Set the starting position randomly inside the screen
pos = [random.randint(0, width), random.randint(0, height)]

# Set the color to green
color = (0, 255, 0)

# Set the scaling factor
scale = 60

# Set the number of iterations
num_iterations = 10000

# Perform the chaos game
for i in range(num_iterations):
    # Pick a random function
    r = random.random()
    if r < 0.01:
        pos = f1(*pos)
    elif r < 0.86:
        pos = f2(*pos)
    elif r < 0.93:
        pos = f3(*pos)
    else:
        pos = f4(*pos)

    # Scale and translate the position to fit inside the screen
    x, y = int(pos[0] * scale + width / 2), int(-pos[1] * scale + height - 30)

    # Draw a point at the new position
    pygame.draw.circle(screen, color, (x, y), 1)

    # Update the display
    pygame.display.flip()

    # Add a delay of delay_time milliseconds
    pygame.time.delay(delay_time)

# Wait for the user to quit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()