import pygame


class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.lives = 3
        self.score = 0
        self.direction = "right"
        self.images = {
            "right": pygame.transform.scale(
                pygame.image.load(
                    "./assets/images/pacman_right.png"), (40, 40)),
            "left": pygame.transform.scale(
                pygame.image.load(
                    "./assets/images/pacman_left.png"), (40, 40)),
            "up": pygame.transform.scale(
                pygame.image.load(
                    "./assets/images/pacman_up.png"), (40, 40)),
            "down": pygame.transform.scale(
                pygame.image.load(
                    "./assets/images/pacman_down.png"), (40, 40)),
        }
        self.current_img = self.images["right"]
    def move_right(self, maze):
        if maze[self.row][self.col + 1] == 0:
            self.col += 1
    def move_left(self, maze):
        if maze[self.row][self.col - 1] == 0:
            self.col -= 1
    def move_up(self, maze):
        if maze[self.row - 1][self.col] == 0:
            self.row -= 1
    def move_down(self, maze):
        if maze[self.row + 1][self.col] == 0:
            self.row += 1
    def lose_life(self):
        self.lives -= 1
    def eat_pacgum(self, points):
        self.score += points
    def is_dead(self):
        return self.lives <= 0
    def draw(self, screen):
        x = self.col * 40
        y = self.row * 40
        screen.blit(self.current_img, (x, y))

