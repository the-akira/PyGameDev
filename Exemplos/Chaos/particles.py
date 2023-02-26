import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Particle Collision")

# Set up the particles
num_particles = 60
max_velocity = 1.5
particles = []
for i in range(num_particles):
    particle = {
        "position": [random.randint(0, size[0]), random.randint(0, size[1])],
        "velocity": [random.uniform(-max_velocity, max_velocity), random.uniform(-max_velocity, max_velocity)],
        "radius": random.randint(5, 13),
        "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    }
    particles.append(particle)

# Start the simulation loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill((0, 0, 0))

    # Move and draw the particles
    for i in range(num_particles):
        particle = particles[i]

        # Update the particle position
        particle["position"][0] += particle["velocity"][0]
        particle["position"][1] += particle["velocity"][1]

        # Check for collisions with the screen edges
        if particle["position"][0] < particle["radius"]:
            particle["position"][0] = particle["radius"]
            particle["velocity"][0] = -particle["velocity"][0]
        elif particle["position"][0] > size[0] - particle["radius"]:
            particle["position"][0] = size[0] - particle["radius"]
            particle["velocity"][0] = -particle["velocity"][0]

        if particle["position"][1] < particle["radius"]:
            particle["position"][1] = particle["radius"]
            particle["velocity"][1] = -particle["velocity"][1]
        elif particle["position"][1] > size[1] - particle["radius"]:
            particle["position"][1] = size[1] - particle["radius"]
            particle["velocity"][1] = -particle["velocity"][1]

        # Check for collisions with other particles
        for j in range(i+1, num_particles):
            other_particle = particles[j]

            dx = other_particle["position"][0] - particle["position"][0]
            dy = other_particle["position"][1] - particle["position"][1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < particle["radius"] + other_particle["radius"]:
                # Collision detected! Swap velocities
                particle["velocity"], other_particle["velocity"] = other_particle["velocity"], particle["velocity"]

        # Draw the particle
        pygame.draw.circle(screen, particle["color"], [int(particle["position"][0]), int(particle["position"][1])], particle["radius"])

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()