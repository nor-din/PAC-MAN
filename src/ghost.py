import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pygame
    from src.ui import AssetManager
    from src.maze import Maze

import random
from typing import Optional
from src.constants import GHOST_MOVE_TICK, Direction


class Ghost:
    def __init__(self, row: int, col: int, color: str) -> None:
        self.row = row
        self.col = col
        self.home = (row, col)
        self.color = color
        self.is_eaten = False
        self.respawn_at = 0

        self.visual_x: Optional[float] = None
        self.visual_y: Optional[float] = None

    def respawn(self) -> None:
        self.row, self.col = self.home
        self.is_eaten = False
        self.visual_x = None
        self.visual_y = None

    def move(self, maze: 'Maze') -> None:
        directions = []
        if maze.can_move(self.row, self.col, Direction.UP):
            directions.append((-1, 0))
        if maze.can_move(self.row, self.col, Direction.DOWN):
            directions.append((1, 0))
        if maze.can_move(self.row, self.col, Direction.LEFT):
            directions.append((0, -1))
        if maze.can_move(self.row, self.col, Direction.RIGHT):
            directions.append((0, 1))

        if directions:
            dr, dc = random.choice(directions)
            self.row += dr
            self.col += dc

    def draw(
            self,
            screen: pygame.Surface,
            assets: 'AssetManager',
            cell_size: int,
            offset_x: int,
            offset_y: int,
            edible: bool = False) -> None:
        if self.is_eaten:
            return

        target_x = self.col * cell_size + offset_x
        target_y = self.row * cell_size + offset_y

        if self.visual_x is None or self.visual_y is None:
            self.visual_x = target_x
            self.visual_y = target_y

        dx = target_x - self.visual_x
        dy = target_y - self.visual_y
        dist = (dx**2 + dy**2)**0.5

        speed = cell_size / GHOST_MOVE_TICK

        if dist < speed:
            self.visual_x = target_x
            self.visual_y = target_y
        elif dist > 0:
            self.visual_x += (dx / dist) * speed
            self.visual_y += (dy / dist) * speed

        img = assets.ghosts["edible"] if edible else assets.ghosts[self.color]
        screen.blit(img, (int(self.visual_x), int(self.visual_y)))
