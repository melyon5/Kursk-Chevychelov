import pygame
import random


class CircleGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.circles = []
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Random Circles")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def add_circle(self):
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        radius = random.randint(10, 100)
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.circles.append((x, y, radius, color))

    def draw_circles(self):
        for x, y, radius, color in self.circles:
            pygame.draw.circle(self.screen, color, (x, y), radius)

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.add_circle()

            self.draw_circles()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = CircleGame(800, 600)
    game.run()
