import pygame

class Pacgum:
    CELL_SIZE = 40
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    def __init__(self, row, col , is_super=False):
        self.row = row
        self.col = col
        self.is_super = is_super
        self.is_eaten = False
        self.points = 50 if is_super else 10
    def eat(self):
        self.is_eaten = True
    def draw(self, screen):
        if not self.is_eaten:
            x = self.col * self.CELL_SIZE + self.CELL_SIZE // 2 + 100
            y = self.row * self.CELL_SIZE + self.CELL_SIZE // 2 + 100
            if self.is_super:
                pygame.draw.circle(screen, self.YELLOW, (x, y), 10)
            else:
                pygame.draw.circle(screen, self.WHITE, (x, y), 5)
