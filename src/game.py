import sys
import pygame
from mazegenerator import MazeGenerator
from src.maze import Maze
from src.player import Player
from src.pacgum import Pacgum
from src.ghost import Ghost

class Images:
    def __init__(self):
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
        self.img_dig = {}
        for d in "0123456789":
            self.img_dig[d] = pygame.image.load(f"assets/images/digit_{d}.png")
            self.img_dig[d] = pygame.transform.scale(self.img_dig[d], (40, 40))
        self.img_heart = pygame.image.load("assets/images/heart.png")
        self.img_heart = pygame.transform.scale(self.img_heart, (50, 50))
        self.img_game_over = pygame.image.load("assets/images/game_over.png")
        self.img_game_over = pygame.transform.scale(self.img_game_over ,(650, 400))
        self.img_menu = pygame.image.load("assets/images/menu.png")
        self.img_menu = pygame.transform.scale(self.img_menu, (500, 150))
        self.img_menu_hover = pygame.image.load("assets/images/menu_hover.png")
        self.img_menu_hover = pygame.transform.scale(self.img_menu_hover, (500, 150))
        self.img_pause = pygame.image.load("assets/images/pause.png")
        self.img_pause = pygame.transform.scale(self.img_pause, (100, 100))
        self.img_pause_title = pygame.image.load("assets/images/pause_title.png")
        self.img_pause_title = pygame.transform.scale(self.img_pause_title, (800, 400))
        self.img_continue = pygame.image.load("assets/images/continue.png")
        self.img_continue = pygame.transform.scale(self.img_continue, (500, 150))
        self.img_continue_hover = pygame.image.load("assets/images/continue_hover.png")
        self.img_continue_hover = pygame.transform.scale(self.img_continue_hover, (500, 150))
        self.img_on = pygame.image.load("assets/images/on.png")
        self.img_on = pygame.transform.scale(self.img_on, (100, 50))
        self.img_off = pygame.image.load("assets/images/off.png")
        self.img_off = pygame.transform.scale(self.img_off, (100, 50))
        self.img_freeze = pygame.image.load("assets/images/freeze.png")
        self.img_freeze = pygame.transform.scale(self.img_freeze, (250, 70))
        self.img_invincible = pygame.image.load("assets/images/invincible.png")
        self.img_invincible = pygame.transform.scale(self.img_invincible, (200, 50))
        self.img_speed = pygame.image.load("assets/images/speed.png")
        self.img_speed = pygame.transform.scale(self.img_speed, (250, 70))

class Cheat:
    def __init__(self):
        self.frezz = False
        self.invincible = False
        self.speed = False

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.images = Images()
        self.cheat = Cheat()
        self.level = 1
        self.gen = MazeGenerator(
            size=(15, 15),
            perfect=False
        )
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
        self.run_pause_menu = True
        self.socre_y = 910
        self.time_y = 10
        self.current_dir = None
        self.step_ghost = 0
        self.step_player = 0
        self.move_player = 1
        self.edible_until = 0
        self.points_ghost = 200
        self.respawn_ms = 8000
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
        self.step = 0
        self.player.lives = 3
        self.cheat.frezz = False
        self.cheat.invincible = False
        self.cheat.speed = False
    def draw(self):
        BLACK = (0, 0 ,0)
        i = 50
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.socre_x = 450
        rect_pause = self.images.img_pause.get_rect()
        rect_pause.x = 5
        rect_pause.y = 5
        self.screen.blit(self.images.img_pause ,rect_pause)
        for d in str(self.player.score):
            self.screen.blit(self.images.img_dig[d], (self.socre_x, self.socre_y))
            self.socre_x += 50
        elapsed = (pygame.time.get_ticks() - self.time_start) // 1000
        time_sec = max(0, (self.time - elapsed))
        self.time_x = 450
        for d in str(time_sec):
            self.screen.blit(self.images.img_dig[d], (self.time_x, self.time_y))
            self.time_x += 50
        eaten = [p for p in self.pacgums
                 if self.player.row == p.row and self.player.col == p.col]
        for p in eaten:
            self.pacgums.remove(p)
            self.player.score += p.points
            if p.is_super:
                self.edible_until = pygame.time.get_ticks() + 7000
        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        now = pygame.time.get_ticks()
        edible = now < self.edible_until
        for ghost in self.ghosts:
            if ghost.is_eaten and now < ghost.respawn_at:
                continue
            if ghost.is_eaten and now >= ghost.respawn_at:
                ghost.respawn()
            if (ghost.row == self.player.row and ghost.col == self.player.col):
                if edible:
                    self.player.score += self.points_ghost
                    ghost.is_eaten = True
                    ghost.respawn_at = now + self.respawn_ms
                else:
                    if not self.cheat.invincible:
                        self.player.row = self.middel_row
                        self.player.col = self.middel_col
                        self.current_dir = None
                        for ghost in self.ghosts:
                            ghost.respawn()
                        self.player.lives -= 1
                        self.cheat.frezz = False
            ghost.draw(self.screen, edible and not ghost.is_eaten)
        for _ in range(self.player.lives):
            self.screen.blit(self.images.img_heart, (370 + i, 58))
            i += 50
        self.player.draw(self.screen)
        if time_sec <= 0 or self.player.lives == 0:
            self.run_game = False
            self.run_game_over = True
            self.game_over()
        self.screen.blit(self.images.img_freeze, (-30, 200))
        self.screen.blit(self.images.img_invincible, (0, 400))
        self.screen.blit(self.images.img_speed, (-30, 600))
        if self.cheat.frezz:
            self.screen.blit(self.images.img_on, (30, 300))
        if not self.cheat.frezz:
            self.screen.blit(self.images.img_off, (30, 300))
        if self.cheat.invincible:
            self.screen.blit(self.images.img_on, (30, 500))
        if not self.cheat.invincible:
            self.screen.blit(self.images.img_off, (30, 500))
        if self.cheat.speed:
            self.screen.blit(self.images.img_on, (30, 700))
        if not self.cheat.speed:
            self.screen.blit(self.images.img_off, (30, 700))
        pygame.display.update()
    def main_menu(self):
        while self.run_menu:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            self.screen.blit(self.images.img_title, (250, 10))
            rect_start = self.images.img_start.get_rect()
            rect_start_hover = self.images.img_start_hover.get_rect()
            rect_start.x = 330
            rect_start.y = 200
            rect_start_hover.x = 330
            rect_start_hover.y = 200
            self.screen.blit(self.images.img_start, rect_start)
            if rect_start.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_start_hover, rect_start_hover)
            rect_highscore = self.images.img_highscore.get_rect()
            rect_highscore_hover = self.images.img_highscore_hover.get_rect()
            rect_highscore.x = 330
            rect_highscore.y = 400
            rect_highscore_hover.x = 330
            rect_highscore_hover.y = 400
            self.screen.blit(self.images.img_highscore, rect_highscore)
            if rect_highscore.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_highscore_hover, rect_highscore_hover)
            rect_instructions = self.images.img_instructions.get_rect()
            rect_instructions_hover = self.images.img_instructions_hover.get_rect()
            rect_instructions.x = 330
            rect_instructions.y = 600
            rect_instructions_hover.x = 330
            rect_instructions_hover.y = 600
            self.screen.blit(self.images.img_instructions, rect_instructions)
            if rect_instructions.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_instructions_hover, rect_instructions_hover)
            rect_exit = self.images.img_exit.get_rect()
            rect_exit_hover = self.images.img_exit_hover.get_rect()
            rect_exit.x = 330
            rect_exit.y = 800
            rect_exit_hover.x = 330
            rect_exit_hover.y = 800
            self.screen.blit(self.images.img_exit, rect_exit)
            if rect_exit.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_exit_hover, rect_exit_hover)
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
        clock = pygame.time.Clock()
        rect_pause = self.images.img_pause.get_rect()
        rect_pause.x = 5
        rect_pause.y = 5
        while self.run_game:
            clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_pause.collidepoint(event.pos):
                        self.run_pause_menu = True
                        self.pause_menu()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.cheat.frezz = not self.cheat.frezz
                    if event.key == pygame.K_i:
                        self.cheat.invincible = not self.cheat.invincible
                    if event.key == pygame.K_e:
                        if self.player.lives < 5:
                            self.player.lives += 1
                    if event.key == pygame.K_s:
                        self.cheat.speed = not self.cheat.speed
                        if self.cheat.speed:
                            self.step_player = 0
                            self.move_player = 2
                        else:
                            self.step_player = 0
                            self.move_player = 1
            if keys[pygame.K_UP] and self.maze.can_move(self.player.row, self.player.col, "up"):
                self.current_dir = "up" 
            if keys[pygame.K_DOWN] and self.maze.can_move(self.player.row, self.player.col, "down"):
                self.current_dir = "down"
            if keys[pygame.K_LEFT] and self.maze.can_move(self.player.row, self.player.col, "left"):
                self.current_dir = "left"
            if keys[pygame.K_RIGHT] and self.maze.can_move(self.player.row, self.player.col, "right"):
                self.current_dir = "right"
            self.step_ghost += 1
            self.step_player += self.move_player
            if self.step_player % 4 == 0:
                if self.current_dir == "up":
                    self.player.move_up(self.maze)
                if self.current_dir == "down":
                    self.player.move_down(self.maze)
                if self.current_dir == "left":
                    self.player.move_left(self.maze)
                if self.current_dir == "right":
                    self.player.move_right(self.maze)
            if self.step_ghost % 4 == 0:
                if not self.cheat.frezz:
                    for ghost in self.ghosts:
                        ghost.move(self.maze)
            self.player.invincible = self.cheat.invincible
            self.draw()
    def pause_menu(self):
        pause_start = pygame.time.get_ticks()
        rect_continue_hover = self.images.img_continue_hover.get_rect()
        rect_continue_hover.x = 275
        rect_continue_hover.y = 350
        rect_menu_hover = self.images.img_menu_hover.get_rect()
        rect_menu_hover.x = 275
        rect_menu_hover.y = 650
        while self.run_pause_menu:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            self.screen.blit(self.images.img_pause_title, (125, -75))
            self.screen.blit(self.images.img_continue, (275, 350))
            self.screen.blit(self.images.img_menu, (275, 650))
            if rect_continue_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_continue_hover, rect_continue_hover)
            if rect_menu_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_menu_hover, rect_menu_hover)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_continue_hover.collidepoint(event.pos):
                        self.run_pause_menu = False
                    if rect_menu_hover.collidepoint(event.pos):
                        self.run_pause_menu = False
                        self.run_game = False
                        self.run_menu = True
                        self.main_menu()
            pygame.display.update()
        self.time_start += pygame.time.get_ticks() - pause_start
    def game_over(self):
        while self.run_game_over:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            self.screen.blit(self.images.img_game_over, (175, 90))
            rect_menu = self.images.img_menu.get_rect()
            rect_menu.x = 250
            rect_menu.y = 600
            rect_menu_hover = self.images.img_menu_hover.get_rect()
            rect_menu_hover.x = 250
            rect_menu_hover.y = 600
            self.screen.blit(self.images.img_menu, rect_menu)
            if rect_menu_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_menu_hover, rect_menu_hover)
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