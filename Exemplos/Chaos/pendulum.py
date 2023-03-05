import pygame
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Pendulum Simulation")

# Define the properties of the pendulum
pendulum_length = 200
pendulum_angle = math.pi / 1.3
pendulum_angular_velocity = 0
pendulum_angular_acceleration = 0
pendulum_mass = 10
pendulum_radius = 20
pendulum_color = WHITE

# Set up the clock
clock = pygame.time.Clock()

# Define a function to calculate the position of the pendulum
def calculate_pendulum_position():
    global pendulum_angle, pendulum_angular_velocity, pendulum_angular_acceleration
    gravity = 9.81
    pendulum_angular_acceleration = (-1 * gravity / pendulum_length) * math.sin(pendulum_angle)
    pendulum_angular_velocity += pendulum_angular_acceleration
    pendulum_angle += pendulum_angular_velocity

# Define a function to draw the pendulum
def draw_pendulum():
    x = screen_width // 2 + pendulum_length * math.sin(pendulum_angle)
    y = screen_height // 2 + pendulum_length * math.cos(pendulum_angle)
    pygame.draw.line(screen, pendulum_color, (screen_width // 2, screen_height // 2), (x, y), 5)
    pygame.draw.circle(screen, pendulum_color, (int(x), int(y)), pendulum_radius)

# Define the main game loop
def game_loop():
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Calculate the position of the pendulum
        calculate_pendulum_position()
        
        # Draw the pendulum
        screen.fill(BLACK)
        draw_pendulum()
        
        # Update the display
        pygame.display.update()
        
        # Set the frame rate
        clock.tick(60)

# Start the game loop
game_loop()