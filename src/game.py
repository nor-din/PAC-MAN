import sys
import json
import pygame
from mazegenerator import MazeGenerator
from src.maze import Maze
from src.player import Player
from src.pacgum import Pacgum
from src.ghost import Ghost
from src.ui import Images
from src.cheat import Cheat
from src.constants import STARTING_LIVES, DEFAULT_TIME_LIMIT, GHOST_POINTS, GHOST_RESPAWN_MS, SUPER_PACGUM_DURATION_MS, FPS, PLAYER_SPEED_TICKS, GHOST_SPEED_TICKS, PLAYER_DEFAULT_MOVE, PLAYER_CHEAT_MOVE


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
        self.time = DEFAULT_TIME_LIMIT
        self.running = True
        self.run_menu = True
        self.run_game = True
        self.run_game_over = True
        self.run_pause_menu = True
        self.run_instruction = True
        self.socre_y = 910
        self.time_y = 10
        self.current_dir = None
        self.step_ghost = 0
        self.step_player = 0
        self.move_player = PLAYER_DEFAULT_MOVE
        self.edible_until = 0
        self.points_ghost = GHOST_POINTS
        self.respawn_ms = GHOST_RESPAWN_MS
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
        self.player.lives = STARTING_LIVES
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
                self.edible_until = pygame.time.get_ticks() + SUPER_PACGUM_DURATION_MS
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
                        self.player.teleport(self.middel_row, self.middel_col)
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
                    if rect_instructions.collidepoint(event.pos):
                        self.run_menu = False
                        self.run_instruction = True
                        self.instructions()
                    if rect_exit.collidepoint(event.pos):
                        sys.exit(0)
            pygame.display.update()
    def instructions(self):
        while self.run_instruction:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            self.screen.blit(self.images.img_instructions_title, (100, 10))
            self.screen.blit(self.images.img_controls, (150, 250))
            self.screen.blit(self.images.img_menu, (250, 800))
            rect_menu_hover = self.images.img_menu_hover.get_rect()
            rect_menu_hover.x = 250
            rect_menu_hover.y = 800
            if rect_menu_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_menu_hover, rect_menu_hover)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_menu_hover.collidepoint(event.pos):
                        self.run_instruction = False
                        self.run_menu = True
                        self.main_menu()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
            pygame.display.update()
    def game(self):
        clock = pygame.time.Clock()
        rect_pause = self.images.img_pause.get_rect()
        rect_pause.x = 5
        rect_pause.y = 5
        while self.run_game:
            clock.tick(FPS)
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
                            self.move_player = PLAYER_CHEAT_MOVE
                        else:
                            self.step_player = 0
                            self.move_player = PLAYER_DEFAULT_MOVE
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
            if self.step_player % PLAYER_SPEED_TICKS == 0:
                if self.current_dir == "up":
                    self.player.move_up(self.maze)
                if self.current_dir == "down":
                    self.player.move_down(self.maze)
                if self.current_dir == "left":
                    self.player.move_left(self.maze)
                if self.current_dir == "right":
                    self.player.move_right(self.maze)
            if self.step_ghost % GHOST_SPEED_TICKS == 0:
                if not self.cheat.frezz:
                    for ghost in self.ghosts:
                        ghost.move(self.maze)
                        
            if not self.cheat.frezz:
                for ghost in self.ghosts:
                    ghost.update_visual()
            self.player.update_visual(self.move_player)
            
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
        font = pygame.font.Font(None, 95)
        empty = font.render("Enter user", True, (0, 0, 0))
        text = ""
        data = {}
        try:
            with open("highscore.json", "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            with open("highscore.json", "w") as f:
                json.dump({}, f, indent=2)
        while self.run_game_over:
            BLACK = (0, 0 ,0)
            self.screen.fill(BLACK)
            self.screen.blit(self.images.img_game_over, (175, 20))
            self.screen.blit(self.images.img_box, (250, 500))
            rect_save = self.images.img_save.get_rect()
            rect_save.x = 250
            rect_save.y = 700
            rect_save_hover = self.images.img_save_hover.get_rect()
            rect_save_hover.x = 250
            rect_save_hover.y = 700
            self.screen.blit(self.images.img_save, rect_save)
            text_ui = font.render(text, True, (0, 0, 0))
            if rect_save_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_save_hover, rect_save_hover)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_save.collidepoint(event.pos) and len(text) > 0:
                        if text in data:
                            data[text] = max(data[text], self.player.score)
                        else:
                            data[text] = self.player.score
                        data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
                        with open("highscore.json", "w") as f:
                            json.dump(data, f, indent=2)
                        self.run_game_over = False
                        self.run_menu = True
                        self.main_menu()
                if event.type == pygame.TEXTINPUT:
                    if len(text) < 10 and (event.text.isalnum() or event.text == " "):
                        text += event.text
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
            text = text.lower()
            if len(text) == 0:
                self.screen.blit(empty, (300, 545))
            if len(text) > 0:
                self.screen.blit(text_ui, (300, 545))
            pygame.display.update()
    def run(self):
        
        while self.running:
            self.main_menu()