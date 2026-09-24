"""Module for wrapping and rendering the 2D grid from the maze generator."""
import pygame


class Maze:
    """Wrapper for the externally generated maze grid."""

    def __init__(self, grid: list[list[int]]) -> None:
        """Initialize the maze.

        Args:
            grid: The 2D integer list representing walls and paths.

        Returns:
            None.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.wallv_img = pygame.transform.scale(
            pygame.image.load('assets/images/wall_v.png'), (4, 40))
        self.wallh_img = pygame.transform.scale(
            pygame.image.load('assets/images/wall_h.png'), (40, 4))

    def is_blocked(self, row: int, col: int) -> bool:
        """Check if a specific tile is a wall.

        Args:
            row: Tile row.
            col: Tile column.

        Returns:
            True if the tile is a wall, False otherwise.
        """
        return self.grid[row][col] == 15

    def can_move(self, row: int, col: int, direction: str) -> bool:
        """Check if an entity can move in a given direction from a tile.

        Args:
            row: Current tile row.
            col: Current tile column.
            direction: 'up', 'down', 'left', or 'right'.

        Returns:
            True if the adjacent tile in that direction is open.
        """
        cell = self.grid[row][col]
        if direction == 'up':
            return cell & 1 == 0
        if direction == 'right':
            return cell & 2 == 0
        if direction == 'down':
            return cell & 4 == 0
        if direction == 'left':
            return cell & 8 == 0
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Render the maze walls onto the screen.

        Args:
            screen: The Pygame surface to draw onto.

        Returns:
            None.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                x = col * 40 + 200
                y = row * 40 + 200
                if cell & 1:
                    screen.blit(self.wallh_img, (x, y))
                if cell & 2:
                    screen.blit(self.wallv_img, (x + 40 - 4, y))
                if cell & 4:
                    screen.blit(self.wallh_img, (x, y + 40 - 4))
                if cell & 8:
                    screen.blit(self.wallv_img, (x, y))
