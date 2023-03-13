import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window size and title
size = (600, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Brownian Motion Simulation")

# Set the background color
background = (255, 255, 255)

# Set the number of particles and their size
num_particles = 100
particle_size = 3

# Create a list of particles with random positions
particles = []
for i in range(num_particles):
    x = random.randint(0, size[0])
    y = random.randint(0, size[1])
    particles.append((x, y))

# Run the simulation loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move each particle randomly
    for i in range(num_particles):
        x, y = particles[i]
        x += random.randint(-1, 1)
        y += random.randint(-1, 1)
        x = max(0, min(x, size[0]))
        y = max(0, min(y, size[1]))
        particles[i] = (x, y)

    # Draw the particles on the screen
    screen.fill(background)
    for x, y in particles:
        pygame.draw.circle(screen, (0, 0, 0), (x, y), particle_size)

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()