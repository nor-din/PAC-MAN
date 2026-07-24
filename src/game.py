import sys
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
            perfect=False
        )
        self.backround = pygame.image.load("./assets/images/background.jpg")
        self.maze = Maze(self.gen.maze)
        self.middel_row = self.maze.rows // 2
        self.middel_col = self.maze.cols // 2
        if not self.maze.is_blocked(self.middel_row, self.middel_col):
            self.player = Player(self.middel_row, self.middel_col)
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
        self.time_start = 0
        self.time = 5
        self.running = True
        self.run_game = True
    def _place_pacgums(self):
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if not (self.player.row == row and self.player.col == col):
                    if not self.maze.is_blocked(row, col):
                        if (row, col) in self.corners:
                            self.pacgums.append(Pacgum(row, col, True))
                        else:
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
        font = pygame.font.Font(None, 36)
        socre_live = font.render(f"Score: {self.player.score}", True, (255,255,255))
        self.screen.blit(socre_live, (10, 770))
        elapsed = (pygame.time.get_ticks() - self.time_start) // 1000
        time_sec = (self.time - elapsed)
        time_live = font.render(f"Time left: {time_sec}", True, (255,255,255))
        self.screen.blit(time_live, (350, 10))
        for p in self.pacgums:
            if (self.player.row == p.row and self.player.col == p.col):
                self.pacgums.remove(p)
                self.player.score += p.points
        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        for ghost in self.ghosts:
            if (ghost.row == self.player.row and ghost.col == self.player.col): 
                print(self.player.lives)
                self.player.row = self.middel_row
                self.player.col = self.middel_col
            ghost.draw(self.screen)
        self.player.draw(self.screen)
        if time_sec <= 0:
            self.game_over()
        pygame.display.update()
    def main_menu(self):
        while self.running:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.time_start = pygame.time.get_ticks()
                        self.game()
                    if exit_button.collidepoint(event.pos):
                        self.running = False
                        self.run_game = False
                        sys.exit(0)
            font = pygame.font.Font(None, 70)
            title = font.render(f"PAC MAN", True, (255,255,0))
            start = font.render(f"START", True, (255,255,250))
            highscores = font.render(f"HIGHSCORES", True, (255,255,250))
            exit = font.render(f"EXIT", True, (255,255,250))
            start_button = start.get_rect(center=(400, 200))
            highscores_bottun = highscores.get_rect(center=(400, 300))
            exit_button = exit.get_rect(center=(400,600))
            self.screen.blit(title, (300, 20))
            self.screen.blit(start, start_button)
            self.screen.blit(highscores, highscores_bottun)
            self.screen.blit(exit, exit_button)
            pygame.display.update()
    def game(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(7)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
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
    def game_over(self):
        while self.running:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 70)
            over = font.render("Game Over", True, (255, 0,0))
            menu = font.render("MENU", True, (255,255,250))
            menu_button = menu.get_rect(center=(400, 600)) 
            final_score = font.render(f"Score: {self.player.score}", True, (255,255,250))
            self.screen.blit(over ,(300, 20))
            self.screen.blit(final_score, (300, 300))
            self.screen.blit(menu, menu_button)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_button.collidepoint(event.pos):
                        self.main_menu()
            pygame.display.update()
    def run(self):
        
        while self.run_game:
            self.main_menu()