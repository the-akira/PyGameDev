import random
import pygame

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

class Square:
  SQUARE_BORDER_WIDTH = 2
  SQUARE_SIDE_LENGTH = 20
  SQUARE_TOTAL_SIDE_LENGTH = SQUARE_SIDE_LENGTH + SQUARE_BORDER_WIDTH * 2

  def __init__(self, color, position):
    self.color = color
    self.position = position

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.position == other.position

  def draw(self, surface):
    pygame.draw.rect(surface, self.color, (
      self.position.x * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.position.y * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.SQUARE_SIDE_LENGTH,
      self.SQUARE_SIDE_LENGTH
    ))

class Snake:
  COLOR = (161, 230, 0)
  DIRECTIONS = {
    pygame.K_UP: {'name': 'up', 'movement': Point(0, -1), 'opposite': 'down'},
    pygame.K_RIGHT: {'name': 'right', 'movement': Point(1, 0), 'opposite': 'left'},
    pygame.K_DOWN: {'name': 'down', 'movement': Point(0, 1), 'opposite': 'up'},
    pygame.K_LEFT: {'name': 'left', 'movement': Point(-1, 0), 'opposite': 'right'}
  }

  def __init__(self, position, direction='right'):
    self.squares = [Square(self.COLOR, position)]
    self.direction = self.DIRECTIONS[pygame.K_RIGHT]
    self.is_alive = True

  def move(self, key):
    if (key in self.DIRECTIONS and self.DIRECTIONS[key]['name'] != self.direction['opposite']):
      self.direction = self.DIRECTIONS[key]

    new_square = Square(self.COLOR, self.squares[-1].position + self.direction['movement'])

    if (new_square in self.squares or
    new_square.position.x < 0 or new_square.position.x >= Game.WIDTH or
    new_square.position.y < 0 or new_square.position.y >= Game.HEIGHT):
      self.is_alive = False

    self.squares.append(new_square)

    return new_square.position

  def shrink(self):
    self.squares.pop(0)

  def draw(self, surface):
    for square in self.squares:
      square.draw(surface)

class Game:
  BACKGROUND_COLOR = (23, 71, 56)
  FOOD_COLOR = (230, 172, 0)
  HEIGHT = 20
  WIDTH = 30
  SCREEN_HEIGHT = HEIGHT * Square.SQUARE_TOTAL_SIDE_LENGTH
  SCREEN_WIDTH = WIDTH * Square.SQUARE_TOTAL_SIDE_LENGTH

  def __init__(self):
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    pygame.display.set_caption("Snake PyGame")

    pygame.font.init()
    self.font = pygame.font.Font(pygame.font.get_default_font(), 45)

    self.clock = pygame.time.Clock()
    self.reset()

  def run(self):
    while True:
      pygame.time.delay(110)
      self.clock.tick(110)

      self.handle_events()
      self.tick()
      self.draw()

  def reset(self):
    self.direction_key = None
    self.snake = Snake(Point(self.WIDTH / 2, self.HEIGHT / 2))
    self.generate_food()

  def generate_food(self):
    self.food = Square(self.FOOD_COLOR, Point(random.randrange(0, self.WIDTH), random.randrange(0, self.HEIGHT)))

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      elif event.type == pygame.KEYDOWN:
        if self.snake.is_alive and event.key in Snake.DIRECTIONS:
          self.direction_key = event.key
        elif not self.snake.is_alive and event.key == pygame.K_SPACE:
          self.reset()

  def tick(self):
    if self.snake.is_alive:
      if self.snake.move(self.direction_key) == self.food.position:
        self.generate_food()
      else:
        self.snake.shrink()

  def draw(self):
    self.screen.fill(self.BACKGROUND_COLOR)

    if self.snake.is_alive:
      self.snake.draw(self.screen)
      self.food.draw(self.screen)
    else:
      text_label = self.font.render("Aperte Espaço para Reviver", 1, (161, 230, 0))
      self.screen.blit(text_label, (self.SCREEN_WIDTH / 2 - text_label.get_width() / 2, 250))

    pygame.display.update()

Game().run()