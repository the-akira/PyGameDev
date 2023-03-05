import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fireworks")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
colors = [red, green, blue, cyan, yellow, magenta]

# Define a Firework class
class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(colors)
        self.radius = 3
        self.exploded = False
        self.particles = []
        self.num_particles = 90
        self.life = 60

    def launch(self):
        self.y -= 10

        if self.y <= height / random.choice([2,3,4,4.5,5,5.5]):
            self.explode()

    def explode(self):
        self.exploded = True

        for i in range(self.num_particles):
            self.particles.append(Particle(self.x, self.y, self.color))

    def show(self):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (self.x, int(self.y)), self.radius)
        else:
            for particle in self.particles:
                particle.show()

    def update(self):
        if not self.exploded:
            self.launch()
        else:
            for particle in self.particles:
                particle.update()
                if particle.life <= 0:
                    self.particles.remove(particle)

        self.life -= 1

# Define a Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 2
        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-3, 3)
        self.life = 30

    def show(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.1
        self.life -= 1

# Create a list to hold all the fireworks
fireworks = []

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill(black)

    # Add new fireworks randomly
    if random.random() < 0.05:
        fireworks.append(Firework(random.randint(50, width-50), height-10))

    # Update and show fireworks
    for firework in fireworks:
        firework.show()
        firework.update()

        if firework.life <= 0:
            fireworks.remove(firework)

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()