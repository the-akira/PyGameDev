import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set up the window dimensions
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Car Game')

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load images
car_img = pygame.image.load('assets/car.png')
car_width, car_height = 50, 100
car_img = pygame.transform.scale(car_img, (car_width, car_height)).convert_alpha()

background_img = pygame.image.load('assets/background.png')
background_img = pygame.transform.scale(background_img, (window_width, window_height)).convert_alpha()

obstacle_width, obstacle_height = 55, 100
obstacle_colors = {
    "red": pygame.transform.scale(pygame.image.load('assets/car_red.png'), (obstacle_width, obstacle_height)).convert_alpha(),
    "green": pygame.transform.scale(pygame.image.load('assets/car_green.png'), (obstacle_width, obstacle_height)).convert_alpha(),
    "blue": pygame.transform.scale(pygame.image.load('assets/car_blue.png'), (obstacle_width, obstacle_height)).convert_alpha()
}
obstacle_color = random.choice(list(obstacle_colors.keys()))

# Set the initial position and speed of the car and obstacle
car_x = window_width // 2 - car_width // 2
car_y = window_height - car_height - 20
car_speed = 5

background_y1 = 0
background_y2 = -window_height

obstacle_x = random.randint(200, 560)
obstacle_y = -obstacle_height
obstacle_speed = 5

# Scoring
score = 0
score_font = pygame.font.SysFont(None, 46)

# Game states
RUNNING = 0
LOST = 1
WAITING_TO_START = 2

# Set the initial game state
game_state = WAITING_TO_START

def check_collision(car_x, car_y, car_width, car_height, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
    return car_x + car_width > obstacle_x and car_x < obstacle_x + obstacle_width and car_y < obstacle_y + obstacle_height and car_y + car_height > obstacle_y

def restart_game():
    global car_x, car_y, background_y1, background_y2, obstacle_x, obstacle_y, score, game_state, obstacle_speed

    car_x = window_width // 2 - car_width // 2
    car_y = window_height - car_height - 20

    background_y1 = 0
    background_y2 = -window_height

    obstacle_x = random.randint(200, 560)
    obstacle_y = -obstacle_height

    score = 0
    obstacle_speed = 5

    game_state = RUNNING

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_state == LOST or game_state == WAITING_TO_START:
                restart_game()

    if game_state == RUNNING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_RIGHT]:
            car_x += car_speed

        if car_x < 200:
            car_x = 200
        elif car_x > 605 - car_width:
            car_x = 605 - car_width

        background_y1 += 5
        background_y2 += 5
        if background_y1 >= window_height:
            background_y1 = -window_height
        if background_y2 >= window_height:
            background_y2 = -window_height

        obstacle_y += obstacle_speed
        if obstacle_y > window_height:
            obstacle_x = random.randint(200, 560)
            obstacle_y = -obstacle_height
            score += 1
            obstacle_speed += 0.01
            obstacle_color = random.choice(list(obstacle_colors.keys()))

        obstacle_img = obstacle_colors[obstacle_color]

        if check_collision(car_x, car_y, car_width, car_height, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
            game_state = LOST

        window.blit(background_img, (0, background_y1))
        window.blit(background_img, (0, background_y2))
        window.blit(car_img, (car_x, car_y))
        window.blit(obstacle_img, (obstacle_x, obstacle_y))

        game_speed = score_font.render(f"Speed: {obstacle_speed * 12:.2f}", True, (0, 0, 0))
        window.blit(game_speed, (10, 10))

        score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
        window.blit(score_text, (10, 50))

    elif game_state == WAITING_TO_START:
        start_text = score_font.render("Press any key to start", True, (255, 255, 255))
        window.blit(start_text, (window_width // 2 - start_text.get_width() // 2, window_height // 2 - 30))
    else:
        lost_text = score_font.render("Game Over. Press any key to restart", True, (0, 0, 0))
        window.blit(lost_text, (window_width // 2 - lost_text.get_width() // 2, window_height // 2 - 30))

    pygame.display.update()
    clock.tick(FPS)