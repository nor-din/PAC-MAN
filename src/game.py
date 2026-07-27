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
        self.time = 90
        self.running = True
        self.run_menu = True
        self.run_game = True
        self.run_game_over = True
        self.img_dig = {}
        self.socre_y = 875
        self.time_y = 10
        self.current_dir = None
        self.img_title = pygame.image.load("assets/images/title.png")
        self.img_title = pygame.transform.scale(self.img_title ,(550, 150))
        self.img_start = pygame.image.load("assets/images/start.png")
        self.img_start = pygame.transform.scale(self.img_start ,(400, 150))
        self.img_start_hover = pygame.image.load("assets/images/start_hover.png")
        self.img_start_hover = pygame.transform.scale(self.img_start_hover ,(400, 150))
        self.img_highscore = pygame.image.load("assets/images/highscore.png")
        self.img_highscore = pygame.transform.scale(self.img_highscore ,(400, 150))
        self.img_highscore_hover = pygame.image.load("assets/images/highscore_hover.png")
        self.img_highscore_hover = pygame.transform.scale(self.img_highscore_hover ,(400, 150))
        self.img_instructions = pygame.image.load("assets/images/instructions.png")
        self.img_instructions = pygame.transform.scale(self.img_instructions ,(400, 150))
        self.img_instructions_hover = pygame.image.load("assets/images/instructions_hover.png")
        self.img_instructions_hover = pygame.transform.scale(self.img_instructions_hover ,(400, 150))
        self.img_exit = pygame.image.load("assets/images/exit.png")
        self.img_exit = pygame.transform.scale(self.img_exit ,(400, 150))
        self.img_exit_hover = pygame.image.load("assets/images/exit_hover.png")
        self.img_exit_hover = pygame.transform.scale(self.img_exit_hover ,(400, 150))
        for d in "0123456789":
            self.img_dig[d] = pygame.image.load(f"assets/images/digit_{d}.png")
            self.img_dig[d] = pygame.transform.scale(self.img_dig[d], (40, 40))
        self.img_heart = pygame.image.load("assets/images/heart.png")
        self.img_heart = pygame.transform.scale(self.img_heart, (50, 50))
        self.list_heart = [self.img_heart, self.img_heart, self.img_heart]
        self.img_game_over = pygame.image.load("assets/images/game_over.png")
        self.img_game_over = pygame.transform.scale(self.img_game_over ,(650, 400))
        self.img_menu = pygame.image.load("assets/images/menu.png")
        self.img_menu = pygame.transform.scale(self.img_menu, (400, 150))
        self.img_pause = pygame.image.load("assets/images/pause.png")
        self.img_pause = pygame.transform.scale(self.img_pause, (100, 100))
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
    def rest(self):
        self.player = Player(self.middel_row, self.middel_col)
        self.pacgums = []
        self._place_pacgums()
        self.ghosts = []
        self._place_ghosts()
        self.time_start = pygame.time.get_ticks()
        self.current_dir = None
        self.list_heart = [self.img_heart, self.img_heart, self.img_heart]
    def draw(self):
        BLACK = (0, 0 ,0)
        i = 50
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.socre_x = 450
        for d in str(self.player.score):
            self.screen.blit(self.img_dig[d], (self.socre_x, self.socre_y))
            self.socre_x += 50
        elapsed = (pygame.time.get_ticks() - self.time_start) // 1000
        time_sec = max(0, (self.time - elapsed))
        self.time_x = 450
        for d in str(time_sec):
            self.screen.blit(self.img_dig[d], (self.time_x, self.time_y))
            self.time_x += 50
        for p in self.pacgums:
            if (self.player.row == p.row and self.player.col == p.col):
                self.pacgums.remove(p)
                self.player.score += p.points
        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        for ghost in self.ghosts:
            if (ghost.row == self.player.row and ghost.col == self.player.col): 
                self.player.row = self.middel_row
                self.player.col = self.middel_col
                self.current_dir = None
                self.list_heart.pop()
                self.player.lives -= 1
            ghost.draw(self.screen)
        for img in self.list_heart:
            self.screen.blit(img, (370 + i, 142))
            i += 50
        self.player.draw(self.screen)
        if time_sec <= 0 or self.player.lives == 0:
            self.run_game = False
            self.run_game_over = True
            self.game_over()
        self.screen.blit(self.img_pause, (5, 5))
        pygame.display.update()
    def main_menu(self):
            while self.run_menu:
                BLACK = (0, 0 ,0)
                self.screen.fill(BLACK)
                self.screen.blit(self.img_title, (250, 10))
                rect_start = self.img_start.get_rect()
                rect_start_hover = self.img_start_hover.get_rect()
                rect_start.x = 330
                rect_start.y = 200
                rect_start_hover.x = 330
                rect_start_hover.y = 200
                self.screen.blit(self.img_start, rect_start)
                if rect_start.collidepoint(pygame.mouse.get_pos()):
                    self.screen.blit(self.img_start_hover, rect_start_hover)
                rect_highscore = self.img_highscore.get_rect()
                rect_highscore_hover = self.img_highscore_hover.get_rect()
                rect_highscore.x = 330
                rect_highscore.y = 400
                rect_highscore_hover.x = 330
                rect_highscore_hover.y = 400
                self.screen.blit(self.img_highscore, rect_highscore)
                if rect_highscore.collidepoint(pygame.mouse.get_pos()):
                    self.screen.blit(self.img_highscore_hover, rect_highscore_hover)
                rect_instructions = self.img_instructions.get_rect()
                rect_instructions_hover = self.img_instructions_hover.get_rect()
                rect_instructions.x = 330
                rect_instructions.y = 600
                rect_instructions_hover.x = 330
                rect_instructions_hover.y = 600
                self.screen.blit(self.img_instructions, rect_instructions)
                if rect_instructions.collidepoint(pygame.mouse.get_pos()):
                    self.screen.blit(self.img_instructions_hover, rect_instructions_hover)
                rect_exit = self.img_exit.get_rect()
                rect_exit_hover = self.img_exit_hover.get_rect()
                rect_exit.x = 330
                rect_exit.y = 800
                rect_exit_hover.x = 330
                rect_exit_hover.y = 800
                self.screen.blit(self.img_exit, rect_exit)
                if rect_exit.collidepoint(pygame.mouse.get_pos()):
                    self.screen.blit(self.img_exit_hover, rect_exit_hover)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if rect_start.collidepoint(event.pos):
                            self.run_menu = False
                            self.run_game = True
                            self.rest()
                            self.game()
                        if rect_exit.collidepoint(event.pos):
                            sys.exit(0)
                pygame.display.update()
    def game(self):
        self.time_start = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        while self.run_game:
            clock.tick(7)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.maze.can_move(self.player.row, self.player.col, "up"):
                self.current_dir = "up" 
            if keys[pygame.K_DOWN] and self.maze.can_move(self.player.row, self.player.col, "down"):
                self.current_dir = "down"
            if keys[pygame.K_LEFT] and self.maze.can_move(self.player.row, self.player.col, "left"):
                self.current_dir = "left"
            if keys[pygame.K_RIGHT] and self.maze.can_move(self.player.row, self.player.col, "right"):
                self.current_dir = "right"
            if self.current_dir == "up":
                self.player.move_up(self.maze)
            if self.current_dir == "down":
                self.player.move_down(self.maze)
            if self.current_dir == "left":
                self.player.move_left(self.maze)
            if self.current_dir == "right":
                self.player.move_right(self.maze)
            for ghost in self.ghosts:
                ghost.move(self.maze)
            self.draw()
    def game_over(self):
        while self.run_game_over:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            self.screen.blit(self.img_game_over, (175, -90))
            rect_menu = self.img_menu.get_rect()
            rect_menu.x = 330
            rect_menu.y = 600
            self.screen.blit(self.img_menu, rect_menu)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_menu.collidepoint(event.pos):
                        self.run_game_over = False
                        self.run_menu = True
                        self.main_menu()
            pygame.display.update()
    def run(self):
        
        while self.running:
            self.main_menu()