import pygame


class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.lives = 3
        self.score = 0
        self.direction = "right"
        self.counter = 0
        self.index = 0
    def move_right(self, maze):
        if maze.can_move(self.row, self.col, "right"):
            self.col += 1
            self.direction = "right"
    
    def move_left(self, maze):
        if maze.can_move(self.row, self.col, "left"):
            self.col -= 1
            self.direction = "left"
    
    def move_up(self, maze):
        if maze.can_move(self.row, self.col, "up"):
            self.row -= 1
            self.direction = "up"
    
    def move_down(self, maze):
        if maze.can_move(self.row, self.col, "down"):
            self.row += 1
            self.direction = "down"
    def lose_life(self):
        self.lives -= 1
    def eat_pacgum(self, points):
        self.score += points
    def is_dead(self):
        return self.lives <= 0
    def draw(self, screen):
        anim_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/images/pac_man_open_{self.direction}.png"), (27, 27)),
            pygame.transform.scale(pygame.image.load(f"assets/images/pac_man_close.png"), (27, 27))
        ]
        self.counter += 1
        if self.counter >= 2:
            self.counter = 0
            self.index += 1
        frame = anim_frames[self.index % len(anim_frames)]
        x = self.col * 40 + 200
        y = self.row * 40 + 200
        screen.blit(frame, (x, y))
