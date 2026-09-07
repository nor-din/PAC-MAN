import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pygame
    from src.ui import AssetManager
    from src.maze import Maze

from typing import Optional
from src.constants import PLAYER_MOVE_TICK, Direction


class Player:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.lives = 3
        self.score = 0
        self.direction: Direction = Direction.RIGHT
        self.is_open = True
        self.invincible = False
        self.toggle_time = 0

        self.visual_x: Optional[float] = None
        self.visual_y: Optional[float] = None

    def move_up(self, maze: 'Maze') -> None:
        self.direction = Direction.UP
        if maze.can_move(self.row, self.col, Direction.UP):
            self.row -= 1

    def move_down(self, maze: 'Maze') -> None:
        self.direction = Direction.DOWN
        if maze.can_move(self.row, self.col, Direction.DOWN):
            self.row += 1

    def move_left(self, maze: 'Maze') -> None:
        self.direction = Direction.LEFT
        if maze.can_move(self.row, self.col, Direction.LEFT):
            self.col -= 1

    def move_right(self, maze: 'Maze') -> None:
        self.direction = Direction.RIGHT
        if maze.can_move(self.row, self.col, Direction.RIGHT):
            self.col += 1

    def draw(
            self,
            screen: pygame.Surface,
            assets: 'AssetManager',
            cell_size: int,
            offset_x: int,
            offset_y: int) -> None:
        # Center the slightly smaller player inside the cell
        p_size = int(cell_size * 0.9)
        padding = (cell_size - p_size) // 2
        target_x = self.col * cell_size + offset_x + padding
        target_y = self.row * cell_size + offset_y + padding

        if self.visual_x is None or self.visual_y is None:
            self.visual_x = target_x
            self.visual_y = target_y

        dx = target_x - self.visual_x
        dy = target_y - self.visual_y
        dist = (dx**2 + dy**2)**0.5

        speed = cell_size / PLAYER_MOVE_TICK

        if dist < speed:
            self.visual_x = target_x
            self.visual_y = target_y
        elif dist > 0:
            self.visual_x += (dx / dist) * speed
            self.visual_y += (dy / dist) * speed

        now = pygame.time.get_ticks()
        if now - self.toggle_time > 150:
            self.is_open = not self.is_open
            self.toggle_time = now

        dir_str = self.direction.name.lower()
        if self.is_open:
            if self.invincible:
                img = assets.player[f"open_invincible_{dir_str}"]
            else:
                img = assets.player[f"open_{dir_str}"]
        else:
            if self.invincible:
                img = assets.player["close_invincible"]
            else:
                img = assets.player["close"]

        screen.blit(img, (int(self.visual_x), int(self.visual_y)))
