import pygame
from src.constants import CELL_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y, PLAYER_SIZE, STARTING_LIVES, PLAYER_ANIM_SPEED, PLAYER_SPEED_TICKS

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visual_x = col * CELL_SIZE
        self.visual_y = row * CELL_SIZE
        self.lives = STARTING_LIVES
        self.score = 0
        self.direction = "right"
        self.counter = 0
        self.index = 0
        self.invincible = False

    def update_visual(self, speed_multiplier):
        target_x = self.col * CELL_SIZE
        target_y = self.row * CELL_SIZE
        speed = (CELL_SIZE / PLAYER_SPEED_TICKS) * speed_multiplier
        
        if self.visual_x < target_x:
            self.visual_x = min(target_x, self.visual_x + speed)
        elif self.visual_x > target_x:
            self.visual_x = max(target_x, self.visual_x - speed)
            
        if self.visual_y < target_y:
            self.visual_y = min(target_y, self.visual_y + speed)
        elif self.visual_y > target_y:
            self.visual_y = max(target_y, self.visual_y - speed)

    def teleport(self, row, col):
        self.row = row
        self.col = col
        self.visual_x = col * CELL_SIZE
        self.visual_y = row * CELL_SIZE

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
            pygame.transform.scale(pygame.image.load(f"assets/images/pac_man_open_{self.direction}.png"), (PLAYER_SIZE, PLAYER_SIZE)),
            pygame.transform.scale(pygame.image.load("assets/images/pac_man_close.png"), (PLAYER_SIZE, PLAYER_SIZE))
        ]
        inv_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/images/pac_man_open_{self.direction}_invincible.png"), (PLAYER_SIZE, PLAYER_SIZE)),
            pygame.transform.scale(pygame.image.load("assets/images/pac_man_close_invincible.png"), (PLAYER_SIZE, PLAYER_SIZE))
        ]
        self.counter += 1
        if self.counter >= PLAYER_ANIM_SPEED:
            self.counter = 0
            self.index += 1
        
        if self.invincible:
            frame = inv_frames[self.index % len(inv_frames)]
        if not self.invincible:
            frame = anim_frames[self.index % len(anim_frames)]
        x = self.visual_x + MAZE_OFFSET_X + (CELL_SIZE - PLAYER_SIZE) // 2
        y = self.visual_y + MAZE_OFFSET_Y + (CELL_SIZE - PLAYER_SIZE) // 2
        screen.blit(frame, (x, y))
