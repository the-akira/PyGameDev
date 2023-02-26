import pygame
import random

pygame.init()

size = (800, 800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chaos Game")

# Set up initial points
points = [(100, 100), (700, 100), (400, 700)]
current = random.choice(points)

# Set up colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

# Set up the scaling factor and number of iterations
scale = 0.5
iterations = 100000

# Run the chaos game
for i in range(iterations):
    pygame.draw.circle(screen, colors[random.randint(0, 2)], current, 1)
    next = random.choice(points)
    current = ((current[0] + next[0]) * scale, (current[1] + next[1]) * scale)

# Display the screen
pygame.display.flip()

# Wait for user to close window
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()