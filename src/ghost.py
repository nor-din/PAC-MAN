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
        if not maze.is_wall(self.row - 1, self.col):
            directions.append((-1, 0))
        if not maze.is_wall(self.row + 1, self.col):
            directions.append((1, 0))
        if not maze.is_wall(self.row, self.col - 1):
            directions.append((0, -1))
        if not maze.is_wall(self.row, self.col + 1):
            directions.append((0, 1))
        if directions:
            dr, dc = random.choice(directions)
            self.row += dr
            self.col += dc
    def draw(self, screen):
        x = self.col * 40
        y = self.row * 40
        screen.blit(self.current_img, (x, y))
    