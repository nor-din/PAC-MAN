from src.constants import POINTS_PACGUM, POINTS_SUPER_PACGUM

class Pacgum:
    def __init__(self, row: int, col: int, is_super: bool = False):
        self.row = row
        self.col = col
        self.is_super = is_super
        self.points = POINTS_SUPER_PACGUM if is_super else POINTS_PACGUM

    def draw(self, screen, assets, cell_size: int, offset_x: int, offset_y: int):
        pacgum_size = int(cell_size * 0.5)
        padding = (cell_size - pacgum_size) // 2
        x = self.col * cell_size + offset_x + padding
        y = self.row * cell_size + offset_y + padding
        img = assets.pacgum["super"] if self.is_super else assets.pacgum["normal"]
        screen.blit(img, (x, y))
