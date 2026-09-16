from __future__ import annotations
import sys
import json
import pygame
from mazegenerator import MazeGenerator
from src.maze import Maze
from src.player import Player
from src.pacgum import Pacgum
from src.ghost import Ghost, chase_red, chase_pink, chase_blue, chase_yellow
from src.ui import Images
from src.cheat import Cheat
from src.highscore import get_top_ten
from src.game_config import GameConfig

KEY_TO_CHAR = {
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",

    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
}


class Game:
    config: 'GameConfig'

    def __init__(self, screen: pygame.Surface) -> None:
        # Engine & Modules
        self.screen = screen
        self.images = Images()
        self.cheat = Cheat()

        # Maze & Level
        self.level = 1
        self.gen = MazeGenerator(
            size=(15, 15),
            perfect=False,
            seed=Game.config.seed
        )
        self.maze = Maze(self.gen.maze)
        self.middel_row = 7
        self.middel_col = 7

        # Entities
        self.player = Player(self.middel_row, self.middel_col)
        self.pacgums: list[Pacgum] = []
        self.ghosts: list[Ghost] = []
        self.corners = [
            (0, 0),
            (0, self.maze.cols - 1),
            (self.maze.rows - 1, 0),
            (self.maze.rows - 1, self.maze.cols - 1)
        ]
        self._place_ghosts()
        self._place_pacgums()

        # Game State loops
        self.running = True
        self.run_menu = True
        self.run_game = True
        self.run_game_over = True
        self.run_victory = True
        self.run_pause_menu = True
        self.run_instruction = True
        self.run_highscore = True

        # Game Parameters & Counters
        self.time_start = 0
        self.time = Game.config.level_max_time
        self.current_dir: str | None = None
        self.step_ghost = 0
        self.step_player = 0
        self.save_ticks = Game.config.ghost_speed_ticks
        self.move_player = Game.config.player_default_move
        self.edible_until = 0
        self.points_ghost = Game.config.points_per_ghost
        self.respawn_ms = Game.config.ghost_respawn_ms

    def _place_pacgums(self) -> None:
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if not (self.player.row == row and self.player.col == col):
                    if not self.maze.is_blocked(row, col):
                        if (row, col) in self.corners:
                            self.pacgums.append(
                                Pacgum(
                                    row,
                                    col,
                                    True,
                                    points=Game.config.points_per_super_pacgum
                                ))
                        else:
                            self.pacgums.append(
                                Pacgum(
                                    row,
                                    col,
                                    points=Game.config.points_per_pacgum))

    def _place_ghosts(self) -> None:
        ghosts_config = [
            ("pink", self.corners[0], chase_pink),
            ("red", self.corners[1], chase_red),
            ("yellow", self.corners[2], chase_yellow),
            ("blue", self.corners[3], chase_blue),
        ]

        for name, (row, col), chase_func in ghosts_config:
            new_ghost = Ghost(
                row,
                col,
                f"./assets/images/ghost_{name}.png",
                chasing_function=chase_func
            )
            self.ghosts.append(new_ghost)
            if name == "red":
                Ghost.red_ghost = new_ghost

    def rest(self) -> None:
        self.player = Player(self.middel_row, self.middel_col)
        self.pacgums = []
        self._place_pacgums()
        self.ghosts = []
        self._place_ghosts()
        self.time_start = pygame.time.get_ticks()
        Game.config.ghost_speed_ticks = self.save_ticks
        self.current_dir = None
        self.edible_until = 0
        self.cheat.frezz = False
        self.cheat.invincible = False
        self.cheat.speed = False
        self.cheat.skip_level = False
        self.level = 1

    def next_level(self) -> None:
        self.cheat.skip_level = False
        self.level += 1

        current_ticks = Game.config.ghost_speed_ticks
        Game.config.ghost_speed_ticks = max(5, current_ticks - 2)

        seed = Game.config.seed
        if seed is not None:
            seed = f"{seed}_{self.level}"

        self.gen = MazeGenerator(
            size=(15, 15),
            perfect=False,
            seed=seed
        )
        self.maze = Maze(self.gen.maze)
        self.middel_row = self.maze.rows // 2
        self.middel_col = self.maze.cols // 2

        self.player.row = self.middel_row
        self.player.col = self.middel_col
        self.player.visual_x = self.middel_col * 40
        self.player.visual_y = self.middel_row * 40
        self.player.direction = "right"
        self.current_dir = None
        self.step_player = 0

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

        self.time_start = pygame.time.get_ticks()
        self.step_ghost = 0
        self.edible_until = 0

    def draw(self) -> None:
        self.screen.blit(self.images.img_background, (0, 0))
        self.maze.draw(self.screen)
        font = pygame.font.Font("PixelatedEleganceRegular-ovawB.ttf", 50)
        score_ui = font.render(
            f"SCORE: {self.player.score}", True, (255, 255, 255))
        lives_ui = font.render(f"x{self.player.lives}", True, (255, 255, 255))
        level_title_ui = font.render("level", True, (255, 255, 255))
        if self.level > 10:
            self.run_game = False
            self.run_victory = True
            self.victory()
        if self.level < 10:
            level_ui = font.render(f"0{self.level}", True, (255, 255, 255))
        if self.level == 10:
            level_ui = font.render(f"{self.level}", True, (255, 255, 255))
        self.screen.blit(score_ui, (370, 850))
        self.screen.blit(lives_ui, (450, 100))
        self.screen.blit(level_title_ui, (820, 400))
        self.screen.blit(level_ui, (870, 450))
        self.screen.blit(self.images.img_heart, (360, 85))
        rect_pause = self.images.img_pause.get_rect()
        rect_pause.x = 5
        rect_pause.y = 5
        self.screen.blit(self.images.img_pause, rect_pause)
        elapsed = (pygame.time.get_ticks() - self.time_start) // 1000
        time_sec = max(0, (self.time - elapsed))
        time_ui = font.render(f"TIME: {time_sec}", True, (255, 255, 255))
        self.screen.blit(time_ui, (370, 10))
        eaten = [
            p for p in self.pacgums if abs(
                self.player.visual_x -
                p.col *
                40) < 15 and abs(
                self.player.visual_y -
                p.row *
                40) < 15]
        for p in eaten:
            self.pacgums.remove(p)
            self.player.score += p.points
            if p.is_super:
                self.edible_until = (pygame.time.get_ticks() +
                                     Game.config.super_pacgum_duration_ms)
                for ghost in self.ghosts:
                    if ghost.current_dir:
                        ghost.current_dir = (
                            -ghost.current_dir[0], -ghost.current_dir[1])

        if len(self.pacgums) == 0 or self.cheat.skip_level:
            self.next_level()

        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        now = pygame.time.get_ticks()
        edible = now < self.edible_until
        for ghost in self.ghosts:
            ghost.is_edible = edible
            if ghost.is_eaten and now < ghost.respawn_at:
                continue
            if ghost.is_eaten and now >= ghost.respawn_at:
                ghost.respawn()
            if abs(
                    ghost.visual_x -
                    self.player.visual_x) < 20 and abs(
                    ghost.visual_y -
                    self.player.visual_y) < 20:
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

    def main_menu(self) -> None:
        while self.run_menu:
            self.screen.blit(self.images.img_background, (0, 0))
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
                self.screen.blit(
                    self.images.img_highscore_hover,
                    rect_highscore_hover)
            rect_instructions = self.images.img_instructions.get_rect()
            rect_instructions_hover = \
                self.images.img_instructions_hover.get_rect()
            rect_instructions.x = 330
            rect_instructions.y = 600
            rect_instructions_hover.x = 330
            rect_instructions_hover.y = 600
            self.screen.blit(self.images.img_instructions, rect_instructions)
            if rect_instructions.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(
                    self.images.img_instructions_hover,
                    rect_instructions_hover)
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
                    if rect_highscore.collidepoint(event.pos):
                        self.run_menu = False
                        self.run_highscore = True
                        self.highscore()
                    if rect_exit.collidepoint(event.pos):
                        sys.exit(0)
            pygame.display.update()

    def instructions(self) -> None:
        space = False
        while self.run_instruction:
            self.screen.blit(self.images.img_background, (0, 0))
            self.screen.blit(self.images.img_instructions_title, (100, 10))
            self.screen.blit(self.images.img_menu, (250, 800))
            rect_menu_hover = self.images.img_menu_hover.get_rect()
            rect_menu_hover.x = 250
            rect_menu_hover.y = 800
            if not space:
                self.screen.blit(self.images.img_controls, (0, 250))
            if space:
                self.screen.blit(self.images.img_rules, (125, 250))
            if rect_menu_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_menu_hover, rect_menu_hover)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_menu_hover.collidepoint(event.pos):
                        self.run_instruction = False
                        self.run_menu = True
                        self.main_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space = not space
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
            pygame.display.update()

    def highscore(self) -> None:
        font = pygame.font.Font("PixelatedEleganceRegular-ovawB.ttf", 40)
        font_empty = pygame.font.Font("PixelatedEleganceRegular-ovawB.ttf", 70)
        empty_ui = font_empty.render(
            "No High Score Yet!", True, (255, 255, 255))
        list_highscore = get_top_ten()
        while self.run_highscore:
            self.screen.blit(self.images.img_background, (0, 0))
            i = 0
            self.screen.blit(self.images.img_highscore_title, (100, 10))
            self.screen.blit(self.images.img_menu, (250, 800))
            rect_menu_hover = self.images.img_menu_hover.get_rect()
            rect_menu_hover.x = 250
            rect_menu_hover.y = 800
            if len(list_highscore) == 0:
                self.screen.blit(empty_ui, (75, 450))
            if len(list_highscore) > 0:
                _, first_socre = list_highscore[0]
            for element in list_highscore:
                name, score = element
                if first_socre > 0:
                    if score > 0:
                        text_ui = font.render(
                            f"{name} : {score}", True, (255, 255, 255))
                        self.screen.blit(text_ui, (300, 200 + i))
                        i += 60
                else:
                    self.screen.blit(empty_ui, (75, 450))
            if rect_menu_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(self.images.img_menu_hover, rect_menu_hover)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_menu_hover.collidepoint(event.pos):
                        self.run_highscore = False
                        self.run_menu = True
                        self.main_menu()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.run_game = False
                    sys.exit(0)
            pygame.display.update()

    def game(self) -> None:
        rect_pause = self.images.img_pause.get_rect()
        rect_pause.x = 5
        rect_pause.y = 5
        while self.run_game:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rect_pause.collidepoint(event.pos):
                        self.run_pause_menu = True
                        self.pause_menu()
                if event.type == pygame.QUIT:
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
                    if event.key == pygame.K_l:
                        self.cheat.skip_level = True
                    if event.key == pygame.K_s:
                        self.cheat.speed = not self.cheat.speed
                        if self.cheat.speed:
                            self.step_player = 0
                            self.move_player = Game.config.player_cheat_move
                        else:
                            self.step_player = 0
                            self.move_player = Game.config.player_default_move
            if keys[pygame.K_UP] and self.maze.can_move(
                    self.player.row, self.player.col, "up"):
                self.current_dir = "up"
            if keys[pygame.K_DOWN] and self.maze.can_move(
                    self.player.row, self.player.col, "down"):
                self.current_dir = "down"
            if keys[pygame.K_LEFT] and self.maze.can_move(
                    self.player.row, self.player.col, "left"):
                self.current_dir = "left"
            if keys[pygame.K_RIGHT] and self.maze.can_move(
                    self.player.row, self.player.col, "right"):
                self.current_dir = "right"
            self.step_ghost += 1
            self.step_player += self.move_player
            if self.step_player % Game.config.player_speed_ticks == 0:
                if self.current_dir == "up":
                    self.player.move_up(self.maze)
                if self.current_dir == "down":
                    self.player.move_down(self.maze)
                if self.current_dir == "left":
                    self.player.move_left(self.maze)
                if self.current_dir == "right":
                    self.player.move_right(self.maze)
            # Check if ghosts are edible to apply 20% slowdown (multiply ticks
            # by 1.25)
            now_ticks = pygame.time.get_ticks()
            are_ghosts_edible = now_ticks < self.edible_until
            base_ghost_ticks = Game.config.ghost_speed_ticks
            current_ghost_ticks = int(
                base_ghost_ticks *
                1.25) if are_ghosts_edible else base_ghost_ticks

            if self.step_ghost % current_ghost_ticks == 0:
                if not self.cheat.frezz:
                    Ghost.update_shared_mode(
                        pygame.time.get_ticks(), self.level)
                    for ghost in self.ghosts:
                        ghost.workflow(self.maze, self.player)

            if not self.cheat.frezz:
                for ghost in self.ghosts:
                    ghost.update_visual()
            self.player.update_visual(self.move_player)
            self.player.invincible = self.cheat.invincible
            self.draw()

    def pause_menu(self) -> None:
        pause_start = pygame.time.get_ticks()
        rect_continue_hover = self.images.img_continue_hover.get_rect()
        rect_continue_hover.x = 275
        rect_continue_hover.y = 350
        rect_menu_hover = self.images.img_menu_hover.get_rect()
        rect_menu_hover.x = 275
        rect_menu_hover.y = 650
        while self.run_pause_menu:
            self.screen.blit(self.images.img_background, (0, 0))
            self.screen.blit(self.images.img_pause_title, (125, -75))
            self.screen.blit(self.images.img_continue, (275, 350))
            self.screen.blit(self.images.img_menu, (275, 650))
            if rect_continue_hover.collidepoint(pygame.mouse.get_pos()):
                self.screen.blit(
                    self.images.img_continue_hover,
                    rect_continue_hover)
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

    def game_over(self) -> None:
        font = pygame.font.Font("PixelatedEleganceRegular-ovawB.ttf", 50)
        empty = font.render("Enter user", True, (0, 0, 0))
        score_ui = font.render(
            f"SCORE: {self.player.score}", True, (255, 255, 255))
        text = ""
        data = {}
        hs_file = Game.config.highscore_filename
        shift = False
        try:
            with open(hs_file, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(hs_file, "w") as f:
                json.dump({}, f, indent=2)
        while self.run_game_over:
            self.screen.blit(self.images.img_background, (0, 0))
            self.screen.blit(self.images.img_game_over, (175, 20))
            self.screen.blit(self.images.img_box, (250, 500))
            self.screen.blit(score_ui, (370, 425))
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
                        data = dict(
                            list(
                                sorted(
                                    data.items(),
                                    key=lambda item: item[1],
                                    reverse=True)))
                        with open(hs_file, "w") as f:
                            json.dump(data, f, indent=2)
                        self.run_game_over = False
                        self.run_menu = True
                        self.main_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        shift = not shift
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key in KEY_TO_CHAR:
                        if len(text) < 10:
                            if not shift:
                                text += KEY_TO_CHAR[event.key]
                            else:
                                text += KEY_TO_CHAR[event.key].upper()
                    elif event.key == pygame.K_SPACE:
                        if len(text) < 10:
                            text += " "
            if len(text) == 0:
                self.screen.blit(empty, (300, 545))
            if len(text) > 0:
                self.screen.blit(text_ui, (300, 545))
            pygame.display.update()

    def victory(self) -> None:
        font = pygame.font.Font("PixelatedEleganceRegular-ovawB.ttf", 50)
        empty = font.render("Enter user", True, (0, 0, 0))
        score_ui = font.render(
            f"SCORE: {self.player.score}", True, (255, 255, 255))
        text = ""
        data = {}
        hs_file = Game.config.highscore_filename
        shift = False
        try:
            with open(hs_file, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(hs_file, "w") as f:
                json.dump({}, f, indent=2)
        while self.run_victory:
            self.screen.blit(self.images.img_background, (0, 0))
            self.screen.blit(self.images.img_victory, (10, 10))
            self.screen.blit(self.images.img_box, (250, 500))
            self.screen.blit(score_ui, (370, 425))
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
                        data = dict(
                            list(
                                sorted(
                                    data.items(),
                                    key=lambda item: item[1],
                                    reverse=True)))
                        with open(hs_file, "w") as f:
                            json.dump(data, f, indent=2)
                        self.run_victory = False
                        self.run_menu = True
                        self.main_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT:
                        shift = not shift
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key in KEY_TO_CHAR:
                        if len(text) < 10:
                            if not shift:
                                text += KEY_TO_CHAR[event.key]
                            else:
                                text += KEY_TO_CHAR[event.key].upper()
                    elif event.key == pygame.K_SPACE:
                        if len(text) < 10:
                            text += " "
            if len(text) == 0:
                self.screen.blit(empty, (300, 545))
            if len(text) > 0:
                self.screen.blit(text_ui, (300, 545))
            pygame.display.update()

    def run(self) -> None:

        while self.running:
            self.main_menu()
