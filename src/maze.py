import pygame


class Maze:
    """Maze class for MazeGenerator output."""

    CELL_SIZE = 40
    BLUE = (0, 0, 255)

    def __init__(self, grid):
        """Initialize maze."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

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
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE
                s = self.CELL_SIZE

                if cell & 1:
                    pygame.draw.line(
                        screen, self.BLUE,
                        (x, y),
                        (x + s, y), 2
                    )

                if cell & 2:
                    pygame.draw.line(
                        screen, self.BLUE,
                        (x + s, y),
                        (x + s, y + s), 2
                    )

                if cell & 4:
                    pygame.draw.line(
                        screen, self.BLUE,
                        (x, y + s),
                        (x + s, y + s), 2
                    )

                if cell & 8:
                    pygame.draw.line(
                        screen, self.BLUE,
                        (x, y),
                        (x, y + s), 2
                    )

    def get_empty_cells(self):
        """Get all non-blocked cells."""
        empty = []
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.is_blocked(row, col):
                    empty.append((row, col))
        return empty
