import pygame
import math

pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lorenz Attractor")
delay_time = 10

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the initial conditions and parameters
x = 1.0
y = 1.0
z = 1.0
dt = 0.01
sigma = 10
rho = 28
beta = 8/3

# Define the Lorenz equations
def dxdt(x, y, z):
    return sigma * (y - x)

def dydt(x, y, z):
    return x * (rho - z) - y

def dzdt(x, y, z):
    return x * y - beta * z

# Loop until the user closes the window
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Calculate the new position using the Lorenz equations
    dx = dxdt(x, y, z) * dt
    dy = dydt(x, y, z) * dt
    dz = dzdt(x, y, z) * dt
    x += dx
    y += dy
    z += dz

    # Convert the 3D position to a 2D pixel on the screen
    x_pixel = int(screen_width/2 + x*10)
    y_pixel = int(screen_height/2 - y*10)

    # Add a delay of delay_time milliseconds
    pygame.time.delay(delay_time)

    # Draw a point on the screen
    screen.set_at((x_pixel, y_pixel), white)

    # Update the display
    pygame.display.update()