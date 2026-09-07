import pygame
from src.constants import CELL_SIZE, MAZE_OFFSET_X, MAZE_OFFSET_Y

class Maze:
    """Maze class for MazeGenerator output."""

    def __init__(self, grid):
        """Initialize maze."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.wallv_img = pygame.transform.scale(
            pygame.image.load("assets/images/wall_v.png"), (4, CELL_SIZE))
        self.wallh_img = pygame.transform.scale(
            pygame.image.load("assets/images/wall_h.png"), (CELL_SIZE, 4))
        

    def is_blocked(self, row, col):
        """Check if cell is fully blocked."""
        return self.grid[row][col] == 15

    def can_move(self, row, col, direction):
        """Check if can move in direction."""
        cell = self.grid[row][col]

        if direction == "up":
            return cell & 1 == 0

        if direction == "right":
            return cell & 2 == 0

        if direction == "down":
            return cell & 4 == 0

        if direction == "left":
            return cell & 8 == 0

        return False

    def draw(self, screen):
        """Draw maze walls as lines."""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                x = col * CELL_SIZE + MAZE_OFFSET_X
                y = row * CELL_SIZE + MAZE_OFFSET_Y

                if cell & 1:
                    screen.blit(self.wallh_img, (x, y))

                if cell & 2:
                    screen.blit(self.wallv_img, (x + CELL_SIZE - 4, y))

                if cell & 4:
                    screen.blit(self.wallh_img, (x, y + CELL_SIZE - 4))

                if cell & 8:
                    screen.blit(self.wallv_img, (x, y))

    def get_empty_cells(self):
        """Get all non-blocked cells."""
        empty = []
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.is_blocked(row, col):
                    empty.append((row, col))
        return empty
