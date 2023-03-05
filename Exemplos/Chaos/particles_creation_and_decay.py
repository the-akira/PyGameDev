import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Particles Creation and Decay")

# Set up the clock
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the particle class
class Particle:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = random.randint(1, 5)
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.size -= 0.1
        self.speed -= 0.1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Create a list of particles
particles = []

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Add new particles to the list
    for i in range(10):
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)
        size = random.randint(5, 20)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        particle = Particle(x, y, size, color)
        particles.append(particle)

    # Update the particles
    for particle in particles:
        particle.update()
        if particle.size <= 0:
            particles.remove(particle)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the particles
    for particle in particles:
        particle.draw()

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)