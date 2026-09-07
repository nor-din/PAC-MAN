from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pygame
    from src.ui import AssetManager

from typing import List, Tuple
from src.constants import Direction


class Maze:
    """Maze class for MazeGenerator output."""

    def __init__(self, grid: List[List[int]]) -> None:
        """Initialize maze."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def is_blocked(self, row: int, col: int) -> bool:
        """Check if cell is fully blocked."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return True
        return self.grid[row][col] == 15

    def can_move(self, row: int, col: int, direction: Direction) -> bool:
        """Check if can move in direction."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False

        cell = self.grid[row][col]

        if direction == Direction.UP:
            return cell & 1 == 0
        if direction == Direction.RIGHT:
            return cell & 2 == 0
        if direction == Direction.DOWN:
            return cell & 4 == 0
        if direction == Direction.LEFT:
            return cell & 8 == 0

        return False

    def draw(
            self,
            screen: 'pygame.Surface',
            assets: 'AssetManager',
            cell_size: int,
            offset_x: int,
            offset_y: int) -> None:
        """Draw maze walls as lines."""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                x = col * cell_size + offset_x
                y = row * cell_size + offset_y

                wall_thick = max(1, cell_size // 10)

                # 1 = top wall
                if cell & 1:
                    screen.blit(assets.maze["wall_h"], (x, y))

                # 2 = right wall
                if cell & 2:
                    screen.blit(assets.maze["wall_v"], (x + cell_size - wall_thick, y))

                # 4 = bottom wall
                if cell & 4:
                    screen.blit(assets.maze["wall_h"], (x, y + cell_size - wall_thick))

                # 8 = left wall
                if cell & 8:
                    screen.blit(assets.maze["wall_v"], (x, y))

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """Get all non-blocked cells."""
        empty = []
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.is_blocked(row, col):
                    empty.append((row, col))
        return empty
