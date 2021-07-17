import pygame

def bouncing_rect():
    global x_speed, y_speed, rect_speed
    moving_rect.x += x_speed
    moving_rect.y += y_speed

    # Colisão com as bordas da tela
    if moving_rect.right >= WIDTH or moving_rect.left <= 0:
        x_speed *= -1
    if moving_rect.bottom >= HEIGHT or moving_rect.top <= 0:
        y_speed *= -1

    # Movendo o segundo retângulo (rect)
    rect.y += rect_speed 
    if rect.top <= 0 or rect.bottom >= HEIGHT:
        rect_speed *= -1

    # Colisão com o retângulo (rect)
    collision_tolerance = 10
    if moving_rect.colliderect(rect):
        if abs(rect.top - moving_rect.bottom) < collision_tolerance and y_speed > 0:
            y_speed *= -1
        if abs(rect.bottom - moving_rect.top) < collision_tolerance and y_speed < 0:
            y_speed *= -1
        if abs(rect.right - moving_rect.left) < collision_tolerance and x_speed < 0:
            x_speed *= -1
        if abs(rect.left - moving_rect.right) < collision_tolerance and x_speed > 0:
            x_speed *= -1

    pygame.draw.rect(window, (255, 255, 255), moving_rect)
    pygame.draw.rect(window, (255, 0, 0), rect)

pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Colisão')

moving_rect = pygame.Rect(350, 350, 100, 100)
x_speed, y_speed = 5, 4

rect = pygame.Rect(300, 600, 200, 100)
rect_speed = 2

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((30, 30, 30))
    bouncing_rect()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()