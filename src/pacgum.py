import pygame
import src.game

class Pacgum:
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, row, col, is_super=False, points=10):
        self.row = row
        self.col = col
        self.is_super = is_super
        self.is_eaten = False
        self.points = points
        if is_super:
            self.img = pygame.image.load("assets/images/super_pacgum.png")
        else:
            self.img = pygame.image.load("assets/images/pacgum.png")
        self.img = pygame.transform.scale(self.img, (30, 30))

    def eat(self):
        self.is_eaten = True

    def draw(self, screen):
        if not self.is_eaten:
            x = self.col * 40 + 200 + (40 - 30) // 2
            y = self.row * 40 + 200 + (40 - 30) // 2
            screen.blit(self.img, (x, y))