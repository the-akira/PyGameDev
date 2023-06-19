import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (235, 235, 235)
BLACK = (0, 0, 0)

class Book:
    def __init__(self):
        self.pages = []
        self.current_page = 0

    def add_page(self, text, image):
        self.pages.append((text, image))

    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1

    def get_current_page(self):
        return self.pages[self.current_page]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Book Simulator")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_size = 29
        self.font = pygame.font.Font(None, self.font_size)
        self.book = Book()
        self.book.add_page('"What is impossible with man is possible with God."', "images/image1.jpg")
        self.book.add_page('"My command is this: Love each other as I have loved you."', "images/image2.jpg")
        self.book.add_page('"You then, my son, be strong in the grace that is in Christ Jesus."', "images/image3.jpg")
        self.book.add_page('"The light shines in the darkness, and the darkness has not overcome it."', "images/image4.jpg")
        self.book.add_page('"Do to others as you would have them do to you."', "images/image5.jpg")
        self.book.add_page('"He gives power to the weak and strength to the powerless."', "images/image6.jpg")
        self.book.add_page('"If God is for us, who can be against us?"', "images/image7.jpg")
        self.book.add_page('"Everything is possible for him who believes."', "images/image8.jpg")
        self.fade_alpha = 0
        self.fade_direction = 0

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.book.current_page != len(self.book.pages) - 1:
                        self.book.next_page()
                        self.fade_direction = 1
                elif event.key == pygame.K_LEFT:
                    if self.book.current_page != 0:
                        self.book.previous_page()
                        self.fade_direction = 1

    def update(self):
        if self.fade_alpha >= 255:
            self.fade_direction = 0
            self.fade_alpha = 0
        elif self.fade_alpha <= 15:
            self.fade_alpha = 15

        if self.fade_direction != 0:
            self.fade_alpha += 20 * self.fade_direction

    def render(self):
        self.screen.fill(WHITE)

        page_text, page_image = self.book.get_current_page()
        self.draw_text(page_text, 40, 30)

        image = pygame.transform.scale(pygame.image.load(page_image),(370,485))
        self.screen.blit(image, (40, 80))

        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.set_alpha(abs(self.fade_alpha))
        fade_surface.fill(BLACK)
        self.screen.blit(fade_surface, (0, 0))

        pygame.display.flip()

    def draw_text(self, text, x, y):
        lines = text.split("\n")
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, BLACK)
            self.screen.blit(text_surface, (x, y + i * 30))

if __name__ == '__main__':
    game = Game()
    game.run()
    pygame.quit()