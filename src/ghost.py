import pygame
import random


class Ghost:
    def __init__(self, row, col, img_path):
        self.row = row
        self.col = col
        self.is_edible = False
        self.is_eaten = False
        self.normal_img = pygame.transform.scale(
            pygame.image.load(img_path), (40, 40)
        )
        self.current_img = self.normal_img
    def make_edible(self):
        self.is_edible = True
    def move(self, maze):
        directions = []
        if maze.can_move(self.row, self.col, "up"):
            directions.append((-1, 0))
        if maze.can_move(self.row, self.col, "down"):
            directions.append((1, 0))
        if maze.can_move(self.row, self.col, "left"):
            directions.append((0, -1))
        if maze.can_move(self.row, self.col, "right"):
            directions.append((0, 1))
        if directions:
            dr, dc = random.choice(directions)
            self.row += dr
            self.col += dc
    def draw(self, screen):
        x = self.col * 40 + 200
        y = self.row * 40 + 200
        screen.blit(self.current_img, (x, y))
    