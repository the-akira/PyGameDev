import pygame
import math
import random

# Initialize pygame
pygame.init()

# Set up the window display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Solar System Simulation")
font = pygame.font.Font(None, 20)

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 102)
orange = (255, 153, 0)
red = (255, 0, 0)
blue = (102, 178, 255)
green = (176, 245, 64)
pink = (217, 189, 219)

# Define classes
class Planet:
    def __init__(self, name, radius, color, distance, speed):
        self.name = name
        self.radius = radius
        self.color = color
        self.distance = distance
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)
        
    def update(self):
        self.angle += self.speed
        self.x = width // 2 + self.distance * math.cos(self.angle)
        self.y = height // 2 + self.distance * math.sin(self.angle)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        

# Define planets
sun = Planet("Sun", 30, yellow, 0, 0)
mercury = Planet("Mercury", 5, green, 80, 0.02)
venus = Planet("Venus", 10, red, 120, 0.03)
earth = Planet("Earth", 15, blue, 160, 0.02)
mars = Planet("Mars", 10, orange, 200, 0.015)
jupiter = Planet("Jupiter", 22, pink, 255, 0.0019)

planets = [sun, mercury, venus, earth, mars, jupiter]

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update planets
    for planet in planets:
        planet.update()
    
    # Draw background
    screen.fill(black)
    
    # Draw planets
    for planet in planets:
        planet.draw(screen)
        # render text surface
        text_surface = font.render(planet.name, True, white)
        
        # position text surface relative to planet
        text_rect = text_surface.get_rect()
        text_rect.centerx = planet.x
        text_rect.centery = planet.y - planet.radius - 10
        
        # blit text surface onto screen
        screen.blit(text_surface, text_rect)
    
    # Update screen
    pygame.display.update()
    
    # Set frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()