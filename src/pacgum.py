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
        if is_super:
            self.img = pygame.image.load("assets/images/super_pacgum.png")
        else:
            self.img = pygame.image.load("assets/images/pacgum.png")
        self.img = pygame.transform.scale(self.img, (30, 30))
    def eat(self):
        self.is_eaten = True
    def draw(self, screen):
        if not self.is_eaten:
            x = self.col * self.CELL_SIZE + 205
            y = self.row * self.CELL_SIZE + 205
            screen.blit(self.img, (x, y))