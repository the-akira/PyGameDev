from pygame.locals import *
import pygame

WIDTH = 500
HEIGHT = 150
FPS = 60

BLACK = (13, 13, 13)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()
logo = pygame.image.load("icon.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Moonlight Sonata - Beethoven")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
sound = pygame.mixer.Sound('beethoven.ogg') 
sound.set_volume(0.7)
myriad_pro_font = pygame.font.SysFont("Myriad Pro", 48)
text = myriad_pro_font.render("p = play | s = stop", 1, WHITE)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                sound.stop()

    screen.fill(BLACK)
    screen.blit(text, (100, 50))
    pygame.display.flip()

pygame.quit()