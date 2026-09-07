import random
from src.constants import LERP_FACTOR

class Ghost:
    def __init__(self, row: int, col: int, color: str):
        self.row = row
        self.col = col
        self.home = (row, col)
        self.color = color
        self.is_edible = False
        self.is_eaten = False
        self.respawn_at = 0

    def make_edible(self):
        self.is_edible = True

    def respawn(self):
        self.row, self.col = self.home
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

    def draw(self, screen, assets, cell_size: int, offset_x: int, offset_y: int, edible: bool = False):
        if self.is_eaten:
            return
            
        target_x = self.col * cell_size + offset_x
        target_y = self.row * cell_size + offset_y
        
        if not hasattr(self, 'visual_x') or self.visual_x is None:
            self.visual_x = target_x
            self.visual_y = target_y
            
        self.visual_x += (target_x - self.visual_x) * LERP_FACTOR
        self.visual_y += (target_y - self.visual_y) * LERP_FACTOR
        
        img = assets.ghosts["edible"] if edible else assets.ghosts[self.color]
        screen.blit(img, (int(self.visual_x), int(self.visual_y)))
