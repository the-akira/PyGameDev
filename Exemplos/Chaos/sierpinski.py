import pygame
import random

pygame.init()

# Set up the display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chaos Game - Sierpinski Triangle")
delay_time = 15

# Define the three vertices of the triangle
vertices = [(width//2, 0), (0, height), (width, height)]

# Set the starting position randomly inside the triangle
pos = [random.randint(0, width), random.randint(0, height)]

# Set the color to white
color = (255, 255, 255)

# Set the scaling factor
scale = 0.5

# Set the number of iterations
num_iterations = 10000

# Perform the chaos game
for i in range(num_iterations):
    # Pick a random vertex
    vertex = random.choice(vertices)

    # Move halfway towards the vertex
    pos[0] = int((pos[0] + vertex[0]) * scale)
    pos[1] = int((pos[1] + vertex[1]) * scale)

    # Draw a point at the new position
    pygame.draw.circle(screen, color, pos, 1)

    # Update the display
    pygame.display.flip()

    # Delay for delay_time milliseconds
    pygame.time.delay(delay_time)

# Wait for the user to quit
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()