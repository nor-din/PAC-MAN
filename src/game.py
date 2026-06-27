import pygame
from mazegenerator import MazeGenerator
from src.maze import Maze
from src.player import Player
from src.pacgum import Pacgum
from src.ghost import Ghost

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.gen = MazeGenerator(
            size=(15, 15),
            perfect=False,
            seed=42
        )
        self.backround = pygame.image.load("./assets/images/background.jpg")
        self.maze = Maze(self.gen.maze)
        middel_row = self.maze.rows // 2
        middel_col = self.maze.cols // 2
        if not self.maze.is_blocked(middel_row, middel_col):
            self.player = Player(middel_row, middel_col)
        self.pacgums = []
        self.ghosts = []
        self.corners = [
            (0, 0),
            (0, self.maze.cols - 1),
            (self.maze.rows - 1, 0),
            (self.maze.rows - 1, self.maze.cols - 1)
        ]
        self._place_ghosts()
        self._place_pacgums()
        self.time = 90
        self.running = True
    def _place_pacgums(self):
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if not (self.player.row == row and self.player.col == col):
                    if not self.maze.is_blocked(row, col):
                        for ghost in self.ghosts:
                            self.pacgums.append(Pacgum(ghost.row, ghost.col, True))
                        self.pacgums.append(Pacgum(row, col))
    def _place_ghosts(self):
        row, col = self.corners[0]
        if not self.maze.is_blocked(row, col):
            self.ghosts.append(Ghost(row, col, "./assets/images/ghost_pink.png"))
        row, col = self.corners[1]
        if not self.maze.is_blocked(row, col):
            self.ghosts.append(Ghost(row, col, "./assets/images/ghost_green.png"))
        row, col = self.corners[2]
        if not self.maze.is_blocked(row, col):
            self.ghosts.append(Ghost(row, col, "./assets/images/ghost_yellow.png"))
        row, col = self.corners[3]
        if not self.maze.is_blocked(row, col):
            self.ghosts.append(Ghost(row, col, "./assets/images/ghost_blue.png"))
    def draw(self):
        BLACK = (0, 0 ,0)
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.update()
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(7)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player.move_up(self.maze)
            if keys[pygame.K_DOWN]:
                self.player.move_down(self.maze)
            if keys[pygame.K_LEFT]:
                self.player.move_left(self.maze)
            if keys[pygame.K_RIGHT]:
                self.player.move_right(self.maze)
            for ghost in self.ghosts:
                ghost.move(self.maze)
            self.draw()