import pygame
import random

# initialize pygame
pygame.init()

# set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Ball with Trail Effect and Particle Effects')

# define colors
white = (255, 255, 255)
black = (0, 0, 0)

# define the Ball class
class Ball:
    def __init__(self, x, y, r, color, vx, vy):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.trail = []
        self.max_particles = 800
        self.particles = []

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        if self.x < self.r or self.x > width - self.r:
            self.vx = -self.vx
            self.explode()
        if self.y < self.r or self.y > height - self.r:
            self.vy = -self.vy
            self.explode()

        self.trail.append((self.x, self.y))
        if len(self.trail) > 50:
            self.trail.pop(0)

        # update particles
        new_particles = []
        for particle in self.particles:
            if particle.lifetime > 0:
                particle.update()
                new_particles.append(particle)
        self.particles = new_particles[:self.max_particles]

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.r)
        for i in range(len(self.trail) - 1):
            alpha = int(255 * (1 - i / len(self.trail)))
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.line(screen, color, self.trail[i], self.trail[i+1], int(self.r * (1 - i / len(self.trail))))
        for particle in self.particles:
            particle.draw()

    def explode(self):
        num_particles = random.randint(10, 250)
        for i in range(num_particles):
            if len(self.particles) < self.max_particles:
                particle = Particle(self.x, self.y, self.color)
                self.particles.append(particle)

# define the Particle class
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.lifetime = random.randint(30, 150)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self):
        alpha = int(255 * (self.lifetime / 60))
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 2)

# create the ball
ball = Ball(width / 2, height / 2, 30, (0, 255, 0), 5, 5)

# set up the game loop
clock = pygame.time.Clock()
done = False

# game loop
while not done:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # update the ball
    ball.update()

    # draw the screen
    screen.fill(black)
    ball.draw()
    pygame.display.update()

    # wait for a short time
    clock.tick(60)

# quit pygame
pygame.quit()