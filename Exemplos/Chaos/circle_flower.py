import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotating Flower")

# Set up the clock
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

colors = [RED, GREEN, BLUE]

# Define the number of circles and their radius
num_circles = 8
circle_radius = 90

# Define the center of the pattern
center_x, center_y = screen_width // 2, screen_height // 2

# Set the angle increment for each circle
angle_increment = 2 * math.pi / num_circles

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the circles
    for i in range(num_circles):
        angle = i * angle_increment
        x = int(center_x + math.cos(angle) * circle_radius)
        y = int(center_y + math.sin(angle) * circle_radius)
        pygame.draw.circle(screen, random.choice(colors), (x, y), circle_radius, 3)

    # Rotate the circles
    angle_increment += 0.01

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)