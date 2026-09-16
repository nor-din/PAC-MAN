from __future__ import annotations
import pygame


class Pacgum:

    def __init__(
            self,
            row: int,
            col: int,
            is_super: bool = False,
            points: int = 10) -> None:
        self.row = row
        self.col = col
        self.is_super = is_super
        self.is_eaten = False
        self.points = points
        if is_super:
            self.img = pygame.image.load('assets/images/super_pacgum.png')
        else:
            self.img = pygame.image.load('assets/images/pacgum.png')
        self.img = pygame.transform.scale(self.img, (30, 30))

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_eaten:
            x = self.col * 40 + 200 + (40 - 30) // 2
            y = self.row * 40 + 200 + (40 - 30) // 2
            screen.blit(self.img, (x, y))
