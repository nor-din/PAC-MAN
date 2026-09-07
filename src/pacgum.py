import pygame
from src.constants import CELL_SIZE, PACGUM_SIZE, PACGUM_POINTS, SUPER_PACGUM_POINTS, MAZE_OFFSET_X, MAZE_OFFSET_Y

class Pacgum:
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, row, col , is_super=False):
        self.row = row
        self.col = col
        self.is_super = is_super
        self.is_eaten = False
        self.points = SUPER_PACGUM_POINTS if is_super else PACGUM_POINTS
        if is_super:
            self.img = pygame.image.load("assets/images/super_pacgum.png")
        else:
            self.img = pygame.image.load("assets/images/pacgum.png")
        self.img = pygame.transform.scale(self.img, (PACGUM_SIZE, PACGUM_SIZE))

    def eat(self):
        self.is_eaten = True

    def draw(self, screen):
        if not self.is_eaten:
            x = self.col * CELL_SIZE + MAZE_OFFSET_X + (CELL_SIZE - PACGUM_SIZE) // 2
            y = self.row * CELL_SIZE + MAZE_OFFSET_Y + (CELL_SIZE - PACGUM_SIZE) // 2
            screen.blit(self.img, (x, y))