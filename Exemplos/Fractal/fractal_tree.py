import pygame
import math
import random

# initialize pygame
pygame.init()

# set up the display
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Fractal Tree')

# define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 42)

# define the Branch class
class Branch:
    def __init__(self, start, angle, length, level):
        self.start = start
        self.angle = angle
        self.length = length
        self.level = level
        self.children = []
        
    def draw(self):
        end_x = self.start[0] + self.length * math.sin(math.radians(self.angle))
        end_y = self.start[1] - self.length * math.cos(math.radians(self.angle))
        end = (end_x, end_y)
        pygame.draw.line(screen, GREEN, self.start, end, 2)

        if self.level > 0:
            child1 = Branch(end, self.angle - 30, self.length * 0.7, self.level - 1)
            self.children.append(child1)
            child2 = Branch(end, self.angle + 30, self.length * 0.7, self.level - 1)
            self.children.append(child2)

        for child in self.children:
            child.draw()

# set up the tree
start_x = width // 2
start_y = height - 50
trunk = Branch((start_x, start_y), -0, 160, 10)

# set up the game loop
done = False
clock = pygame.time.Clock()

# game loop
while not done:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # draw the screen
    screen.fill(BLACK)
    trunk.draw()
    pygame.display.update()

    # wait for a short time
    clock.tick(60)

# quit pygame
pygame.quit()