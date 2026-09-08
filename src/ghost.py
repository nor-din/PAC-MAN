import pygame
import random
import src.game

class Ghost:
    def __init__(self, row, col, img_path):
        self.row = row
        self.col = col
        self.home = (row, col)
        self.visual_x = col * 40
        self.visual_y = row * 40
        self.is_edible = False
        self.is_eaten = False
        self.respawn_at = 0
        self.normal_img = pygame.transform.scale(
            pygame.image.load(img_path), (40, 40)
        )
        self.edible_img = pygame.transform.scale(
            pygame.image.load("assets/images/ghost_eatble.png"), (40, 40)
        )
        self.current_img = self.normal_img

    def update_visual(self):
        target_x = self.col * 40
        target_y = self.row * 40
        speed = 40 / src.game.Game.config_dict["ghost_speed_ticks"]
        
        if self.visual_x < target_x:
            self.visual_x = min(target_x, self.visual_x + speed)
        elif self.visual_x > target_x:
            self.visual_x = max(target_x, self.visual_x - speed)
            
        if self.visual_y < target_y:
            self.visual_y = min(target_y, self.visual_y + speed)
        elif self.visual_y > target_y:
            self.visual_y = max(target_y, self.visual_y - speed)

    def make_edible(self):
        self.is_edible = True

    def respawn(self):
        self.row, self.col = self.home
        self.visual_x = self.col * 40
        self.visual_y = self.row * 40
        self.is_eaten = False
        self.is_edible = False

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

    def draw(self, screen, edible=False):
        if self.is_eaten:
            return
        x = self.visual_x + 200
        y = self.visual_y + 200
        img = self.edible_img if edible else self.current_img
        screen.blit(img, (x, y))
    