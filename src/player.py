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
        if maze.can_move(self.row, self.col, "right"):
            self.col += 1
            self.direction = "right"
            self.current_img = self.images["right"]
    
    def move_left(self, maze):
        if maze.can_move(self.row, self.col, "left"):
            self.col -= 1
            self.direction = "left"
            self.current_img = self.images["left"]
    
    def move_up(self, maze):
        if maze.can_move(self.row, self.col, "up"):
            self.row -= 1
            self.direction = "up"
            self.current_img = self.images["up"]
    
    def move_down(self, maze):
        if maze.can_move(self.row, self.col, "down"):
            self.row += 1
            self.direction = "down"
            self.current_img = self.images["down"]
    def lose_life(self):
        self.lives -= 1
    def eat_pacgum(self, points):
        self.score += points
    def is_dead(self):
        return self.lives <= 0
    def draw(self, screen):
        x = self.col * 40 + 200
        y = self.row * 40 + 200
        screen.blit(self.current_img, (x, y))

