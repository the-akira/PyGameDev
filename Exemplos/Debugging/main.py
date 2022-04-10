import pygame 
pygame.init()

WIDTH = 835
HEIGHT = 450
FPS = 30
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 33)

def debug(info, x=10, y=10):
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(str(info), True, WHITE)
    debug_rect = debug_surface.get_rect(topleft=(x,y))
    display_surface.blit(debug_surface, debug_rect)

class Bug(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_left = pygame.image.load(f'images/{num}.png').convert_alpha()
            img_left = pygame.transform.scale(img_left, (int(img_left.get_width() * scale), int(img_left.get_height() * scale)))
            img_right = pygame.transform.flip(img_left, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)   
        self.image = self.images_right[self.index]    
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x = x 
        self.rect.y = y
        self.direction = 0

    def update(self):
        dx = 0 
        dy = 0
        walk_cooldown = 4
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            dx -= 6
            self.counter += 1
            self.direction = -1
            if self.rect.left <= 0:
                self.rect.left = 0
        if key[pygame.K_RIGHT]:
            dx += 6
            self.counter += 1
            self.direction = 1
            if self.rect.right >= WIDTH:
                self.rect.right = WIDTH
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1 
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]

        self.rect.x += dx 
        self.rect.y += dy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Debugging')
clock = pygame.time.Clock()

background = pygame.image.load('images/bg.png').convert_alpha()
all_sprites = pygame.sprite.Group()
player = Bug(50, 165, 0.3)
all_sprites.add(player)

running = True 
while running:
    screen.blit(background,(0,0))
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    all_sprites.update()
    all_sprites.draw(screen)
    debug((player.rect.x, player.rect.y))
    debug(pygame.mouse.get_pressed(), 380)
    debug(pygame.mouse.get_pos(), 725)
    pygame.display.flip()

pygame.quit()