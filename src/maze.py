class Maze:
    """Maze class for MazeGenerator output."""

    def __init__(self, grid):
        """Initialize maze."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def is_blocked(self, row, col):
        """Check if cell is fully blocked."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return True
        return self.grid[row][col] == 15

    def can_move(self, row, col, direction):
        """Check if can move in direction."""
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return False
            
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

    def draw(self, screen, assets, cell_size: int, offset_x: int, offset_y: int):
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

    def get_empty_cells(self):
        """Get all non-blocked cells."""
        empty = []
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.is_blocked(row, col):
                    empty.append((row, col))
        return empty
