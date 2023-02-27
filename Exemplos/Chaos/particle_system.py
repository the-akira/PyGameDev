import pygame
import random

# initialize pygame
pygame.init()

# set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Particle System')

# define colors
white = (255, 255, 255)
black = (0, 0, 0)

# define the Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 2
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.alpha = 255
        self.fade_rate = 3
        self.max_lifetime = 60
        self.lifetime = self.max_lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= self.fade_rate
        self.lifetime -= 1

    def draw(self):
        color = self.color + (self.alpha,)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def is_dead(self):
        return self.lifetime <= 0 or self.alpha <= 0

# set up the particle system
particles = []

# set up the game loop
clock = pygame.time.Clock()
done = False

# game loop
while not done:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # update the particles
    for particle in particles:
        particle.update()

    # remove dead particles
    particles = [particle for particle in particles if not particle.is_dead()]

    # add new particles
    if len(particles) < 350:
        for i in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            particle = Particle(x, y, color)
            particles.append(particle)

    # draw the screen
    screen.fill(black)
    for particle in particles:
        particle.draw()
    pygame.display.update()

    # wait for a short time
    clock.tick(60)

# quit pygame
pygame.quit()