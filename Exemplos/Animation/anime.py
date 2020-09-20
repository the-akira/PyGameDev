import pygame

SIZE = WIDTH, HEIGHT = 150, 150 
BACKGROUND_COLOR = pygame.Color('white') 
FPS = 10 

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('sprites/mario1.png'))
        self.images.append(pygame.image.load('sprites/mario2.png'))
        self.images.append(pygame.image.load('sprites/mario3.png'))
        self.images.append(pygame.image.load('sprites/mario4.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 150, 200)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Animation")
    sprite = Sprite()
    group = pygame.sprite.Group(sprite)
    clock = pygame.time.Clock()

    while True:
        screen.fill(BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        group.update() 
        group.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()