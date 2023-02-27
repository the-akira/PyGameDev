import pygame
import random

pygame.init()

# set up the window
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fireworks")

# set up the clock
clock = pygame.time.Clock()

# define the Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = random.randint(3, 7)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.life = random.randint(20, 60)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.15

        self.life -= 0.75

    def draw(self):
        alpha = int(255 * self.life / 60)
        pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], alpha), (int(self.x), int(self.y)), self.radius)

# create a list to hold the particles
particles = []

# create a function to create the particles
def create_particles(x, y):
    for i in range(350):
        particle = Particle(x, y)
        particles.append(particle)

# main game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            create_particles(*event.pos)

    # move the particles
    for particle in particles:
        particle.move()

    # remove particles with life <= 0
    particles = [particle for particle in particles if particle.life > 0]

    # draw the particles
    screen.fill((0, 0, 0))
    for particle in particles:
        particle.draw()

    # update the display
    pygame.display.update()

    # limit the frame rate
    clock.tick(60)