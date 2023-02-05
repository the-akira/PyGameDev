import pygame

def draw_sierpinski(surface, color, points, depth):
    if depth == 0:
        pygame.draw.polygon(surface, color, points, 0)
        return

    x1, y1 = (points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2
    x2, y2 = (points[1][0] + points[2][0]) / 2, (points[1][1] + points[2][1]) / 2
    x3, y3 = (points[2][0] + points[0][0]) / 2, (points[2][1] + points[0][1]) / 2

    draw_sierpinski(surface, color, [(points[0][0], points[0][1]), (x1, y1), (x3, y3)], depth - 1)
    draw_sierpinski(surface, color, [(x1, y1), (points[1][0], points[1][1]), (x2, y2)], depth - 1)
    draw_sierpinski(surface, color, [(x3, y3), (x2, y2), (points[2][0], points[2][1])], depth - 1)

def main():
    pygame.init()
    screen_width, screen_height = 800, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Sierpiński Triangle')
    depth = 8

    points = [(400, 10), (10, 790), (790, 790)]
    color = (0, 255, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((0, 0, 0))
        draw_sierpinski(screen, color, points, depth)
        pygame.display.update()

if __name__ == '__main__':    
    main()