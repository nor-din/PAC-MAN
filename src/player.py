from src.constants import LERP_FACTOR

class Player:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.lives = 3
        self.score = 0
        self.direction = "right"
        self.is_open = True
        self.invincible = False
        self.toggle_time = 0

    def move_up(self, maze):
        self.direction = "up"
        if maze.can_move(self.row, self.col, "up"):
            self.row -= 1

    def move_down(self, maze):
        self.direction = "down"
        if maze.can_move(self.row, self.col, "down"):
            self.row += 1

    def move_left(self, maze):
        self.direction = "left"
        if maze.can_move(self.row, self.col, "left"):
            self.col -= 1

    def move_right(self, maze):
        self.direction = "right"
        if maze.can_move(self.row, self.col, "right"):
            self.col += 1

    def draw(self, screen, assets, cell_size: int, offset_x: int, offset_y: int):
        # Center the slightly smaller player inside the cell
        p_size = int(cell_size * 0.9)
        padding = (cell_size - p_size) // 2
        target_x = self.col * cell_size + offset_x + padding
        target_y = self.row * cell_size + offset_y + padding

        if not hasattr(self, 'visual_x') or self.visual_x is None:
            self.visual_x = target_x
            self.visual_y = target_y

        # Linear interpolation for buttery smooth visuals
        self.visual_x += (target_x - self.visual_x) * LERP_FACTOR
        self.visual_y += (target_y - self.visual_y) * LERP_FACTOR

        import pygame
        now = pygame.time.get_ticks()
        if now - self.toggle_time > 150:
            self.is_open = not self.is_open
            self.toggle_time = now

        if self.is_open:
            if self.invincible:
                img = assets.player[f"open_invincible_{self.direction}"]
            else:
                img = assets.player[f"open_{self.direction}"]
        else:
            if self.invincible:
                img = assets.player["close_invincible"]
            else:
                img = assets.player["close"]

        screen.blit(img, (int(self.visual_x), int(self.visual_y)))
