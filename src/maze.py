import pygame


class Maze:
    CELL_SIZE = 40
    BLUE = (0, 0, 255)
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
    def is_wall(self, row, col):
        return self.grid[row][col] == 1
    def draw(self, screen):
       for row in range(self.rows):
           for col in range(self.cols):
               if self.is_wall(row,col):
                    pygame.draw.rect(
                        screen,
                        self.BLUE,
                        (
                            col * self.CELL_SIZE,
                            row * self.CELL_SIZE,
                            self.CELL_SIZE,
                            self.CELL_SIZE
                        )
                    )
    def get_empty_cells(self):
        empty = []
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.is_wall(row, col):
                    empty.append((row, col))
        return empty
