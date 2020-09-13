import pygame
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, startpos, velocity, startdir):
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.image_load = pygame.image.load("ball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_load, (75,75))
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

all_groups = pygame.sprite.Group()
start, velocity, direction = (250, 250), 5, (random.random(), random.random())
ball = Ball(start, velocity, direction)
all_groups.add(ball)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_groups.update()

    if ball.rect.left <= 100:
        ball.reflect((1, 0))
    if ball.rect.right >= 400:
        ball.reflect((-1, 0))
    if ball.rect.top <= 100:
        ball.reflect((0, 1))
    if ball.rect.bottom >= 400:
        ball.reflect((0, -1))

    window.fill((90,90,90))
    pygame.draw.rect(window, (0, 0, 0), (100, 100, 300, 300), 4)
    all_groups.draw(window)
    pygame.display.flip()