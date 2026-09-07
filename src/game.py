import sys
import pygame
from mazegenerator import MazeGenerator

from src.constants import (
    GameState, FPS, MAX_BOARD_WIDTH, MAX_BOARD_HEIGHT, 
    PLAYER_MOVE_TICK, GHOST_MOVE_TICK, POINTS_GHOST, 
    RESPAWN_DELAY_MS, EDIBLE_DURATION_MS
)
from src.maze import Maze
from src.player import Player
from src.pacgum import Pacgum
from src.ghost import Ghost
from src.ui import AssetManager
from src.cheat import Cheat

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.assets = AssetManager()
        self.cheat = Cheat()
        
        self.state = GameState.MENU
        self.running = True
        
        # Configuration defaults (These will be overwritten when config is injected)
        self.level = 1
        self.max_time = 90
        
        # Will be set dynamically when a level loads
        self.maze = None
        self.player = None
        self.pacgums = []
        self.ghosts = []
        
        # Dynamic Board rendering vars
        self.cell_size = 40
        self.offset_x = 200
        self.offset_y = 200
        
        # Game loop vars
        self.time_start = 0
        self.time_left = 90
        self.step_ghost = 0
        self.step_player = 0
        self.move_player = 1
        self.edible_until = 0
        
        self.points_ghost = POINTS_GHOST
        self.respawn_ms = RESPAWN_DELAY_MS
        
    def load_level(self):
        # Generate maze
        size = 15 # Will be dynamic from config later
        self.gen = MazeGenerator(size=(size, size), perfect=False)
        self.maze = Maze(self.gen.maze)
        
        # Calculate dynamic cell size and offsets to fit screen (1000x1000)
        # Leaving padding for UI
        max_board_width = MAX_BOARD_WIDTH
        max_board_height = MAX_BOARD_HEIGHT
        self.cell_size = min(max_board_width // self.maze.cols, max_board_height // self.maze.rows)
        self.offset_x = (1000 - (self.maze.cols * self.cell_size)) // 2
        self.offset_y = (1000 - (self.maze.rows * self.cell_size)) // 2
        
        # Scale assets once for this level
        self.assets.scale_level_assets(self.cell_size)
        
        middle_row, middle_col = self.maze.rows // 2, self.maze.cols // 2
        self.player = Player(middle_row, middle_col)
        self.player.lives = 3
        
        self.pacgums = []
        self.ghosts = []
        self.corners = [
            (1, 1),
            (1, self.maze.cols - 2),
            (self.maze.rows - 2, 1),
            (self.maze.rows - 2, self.maze.cols - 2),
        ]
        
        self._place_ghosts()
        self._place_pacgums()
        
        self.time_start = pygame.time.get_ticks()
        self.time_left = self.max_time
        
        self.cheat = Cheat() # reset cheats
        self.current_dir = None
        self.state = GameState.PLAYING

    def _place_pacgums(self):
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                if not (self.player.row == row and self.player.col == col):
                    if not self.maze.is_blocked(row, col):
                        if (row, col) in self.corners:
                            self.pacgums.append(Pacgum(row, col, is_super=True))
                        else:
                            self.pacgums.append(Pacgum(row, col))

    def _place_ghosts(self):
        colors = ["pink", "green", "yellow", "blue"]
        for i, corner in enumerate(self.corners):
            r, c = corner
            if not self.maze.is_blocked(r, c):
                self.ghosts.append(Ghost(r, c, colors[i % len(colors)]))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            self._handle_events()
            
            if self.state == GameState.MENU:
                self._draw_menu()
            elif self.state == GameState.INSTRUCTIONS:
                self._draw_instructions()
            elif self.state == GameState.PLAYING:
                self._update_game()
                self._draw_game()
            elif self.state == GameState.PAUSED:
                self._draw_pause()
            elif self.state == GameState.GAME_OVER:
                self._draw_game_over()
                
            pygame.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse(event.pos)
                
            if event.type == pygame.KEYDOWN and self.state == GameState.PLAYING:
                if event.key == pygame.K_f:
                    self.cheat.frezz = not self.cheat.frezz
                elif event.key == pygame.K_i:
                    self.cheat.invincible = not self.cheat.invincible
                elif event.key == pygame.K_e:
                    if self.player.lives < 5:
                        self.player.lives += 1
                elif event.key == pygame.K_s:
                    self.cheat.speed = not self.cheat.speed
                    self.move_player = 2 if self.cheat.speed else 1

    def _handle_mouse(self, pos):
        if self.state == GameState.MENU:
            if self._rect_for_menu("start").collidepoint(pos):
                self.load_level()
            elif self._rect_for_menu("instructions").collidepoint(pos):
                self.state = GameState.INSTRUCTIONS
            elif self._rect_for_menu("exit").collidepoint(pos):
                self.running = False
                sys.exit(0)
        elif self.state == GameState.INSTRUCTIONS:
            if pygame.Rect(250, 800, 500, 150).collidepoint(pos): # menu button
                self.state = GameState.MENU
        elif self.state == GameState.PLAYING:
            if pygame.Rect(5, 5, 100, 100).collidepoint(pos): # pause button
                self.pause_start = pygame.time.get_ticks()
                self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            if pygame.Rect(275, 350, 500, 150).collidepoint(pos): # continue
                self.time_start += pygame.time.get_ticks() - self.pause_start
                self.state = GameState.PLAYING
            elif pygame.Rect(275, 650, 500, 150).collidepoint(pos): # menu
                self.state = GameState.MENU
        elif self.state == GameState.GAME_OVER:
            if pygame.Rect(250, 600, 500, 150).collidepoint(pos): # menu
                self.state = GameState.MENU

    def _rect_for_menu(self, btn):
        if btn == "start": return pygame.Rect(330, 200, 400, 150)
        if btn == "highscore": return pygame.Rect(330, 400, 400, 150)
        if btn == "instructions": return pygame.Rect(330, 600, 400, 150)
        if btn == "exit": return pygame.Rect(330, 800, 400, 150)
        return pygame.Rect(0,0,0,0)

    def _update_game(self):
        keys = pygame.key.get_pressed()
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
        
        if self.step_player % PLAYER_MOVE_TICK == 0 and self.current_dir:
            getattr(self.player, f"move_{self.current_dir}")(self.maze)
            
        if self.step_ghost % GHOST_MOVE_TICK == 0 and not self.cheat.frezz:
            for ghost in self.ghosts:
                ghost.move(self.maze)
                
        self.player.invincible = self.cheat.invincible
        
        # Check timer
        elapsed = (pygame.time.get_ticks() - self.time_start) // 1000
        self.time_left = max(0, (self.max_time - elapsed))
        
        if self.time_left <= 0 or self.player.lives <= 0:
            self.state = GameState.GAME_OVER

    def _draw_game(self):
        self.screen.fill((0,0,0))
        self.maze.draw(self.screen, self.assets, self.cell_size, self.offset_x, self.offset_y)
        
        # UI Overlays
        self.screen.blit(self.assets.img_pause, (5, 5))
        
        socre_x = 450
        for d in str(self.player.score):
            self.screen.blit(self.assets.img_dig[d], (socre_x, 910))
            socre_x += 50
            
        time_x = 450
        for d in str(self.time_left):
            self.screen.blit(self.assets.img_dig[d], (time_x, 10))
            time_x += 50
            
        # Collect pacgums
        eaten = [p for p in self.pacgums if self.player.row == p.row and self.player.col == p.col]
        for p in eaten:
            self.pacgums.remove(p)
            self.player.score += p.points
            if p.is_super:
                self.edible_until = pygame.time.get_ticks() + EDIBLE_DURATION_MS
                
        for pacgum in self.pacgums:
            pacgum.draw(self.screen, self.assets, self.cell_size, self.offset_x, self.offset_y)
            
        # Draw Entities
        now = pygame.time.get_ticks()
        edible = now < self.edible_until
        
        for ghost in self.ghosts:
            if ghost.is_eaten and now >= ghost.respawn_at:
                ghost.respawn()
            elif ghost.is_eaten:
                continue
                
            if ghost.row == self.player.row and ghost.col == self.player.col:
                if edible:
                    self.player.score += self.points_ghost
                    ghost.is_eaten = True
                    ghost.respawn_at = now + self.respawn_ms
                elif not self.cheat.invincible:
                    self.player.row = self.maze.rows // 2
                    self.player.col = self.maze.cols // 2
                    self.current_dir = None
                    for g in self.ghosts:
                        g.respawn()
                    self.player.lives -= 1
                    self.cheat.frezz = False
            
            ghost.draw(self.screen, self.assets, self.cell_size, self.offset_x, self.offset_y, edible)
            
        self.player.draw(self.screen, self.assets, self.cell_size, self.offset_x, self.offset_y)
        
        # Lives
        for i in range(self.player.lives):
            self.screen.blit(self.assets.img_heart, (370 + i*50, 58))
            
        # Cheats overlay
        self.screen.blit(self.assets.img_freeze, (-30, 200))
        self.screen.blit(self.assets.img_invincible, (0, 400))
        self.screen.blit(self.assets.img_speed, (-30, 600))
        
        self.screen.blit(self.assets.img_on if self.cheat.frezz else self.assets.img_off, (30, 300))
        self.screen.blit(self.assets.img_on if self.cheat.invincible else self.assets.img_off, (30, 500))
        self.screen.blit(self.assets.img_on if self.cheat.speed else self.assets.img_off, (30, 700))

    def _draw_menu(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.assets.img_title, (250, 10))
        pos = pygame.mouse.get_pos()
        
        start_rect = self._rect_for_menu("start")
        self.screen.blit(self.assets.img_start_hover if start_rect.collidepoint(pos) else self.assets.img_start, start_rect)
        
        hs_rect = self._rect_for_menu("highscore")
        self.screen.blit(self.assets.img_highscore_hover if hs_rect.collidepoint(pos) else self.assets.img_highscore, hs_rect)
        
        inst_rect = self._rect_for_menu("instructions")
        self.screen.blit(self.assets.img_instructions_hover if inst_rect.collidepoint(pos) else self.assets.img_instructions, inst_rect)
        
        exit_rect = self._rect_for_menu("exit")
        self.screen.blit(self.assets.img_exit_hover if exit_rect.collidepoint(pos) else self.assets.img_exit, exit_rect)

    def _draw_instructions(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.assets.img_instructions_title, (100, 10))
        self.screen.blit(self.assets.img_controls, (150, 250))
        
        menu_rect = pygame.Rect(250, 800, 500, 150)
        pos = pygame.mouse.get_pos()
        self.screen.blit(self.assets.img_menu_hover if menu_rect.collidepoint(pos) else self.assets.img_menu, menu_rect)

    def _draw_pause(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.assets.img_pause_title, (125, -75))
        
        pos = pygame.mouse.get_pos()
        cont_rect = pygame.Rect(275, 350, 500, 150)
        self.screen.blit(self.assets.img_continue_hover if cont_rect.collidepoint(pos) else self.assets.img_continue, cont_rect)
        
        menu_rect = pygame.Rect(275, 650, 500, 150)
        self.screen.blit(self.assets.img_menu_hover if menu_rect.collidepoint(pos) else self.assets.img_menu, menu_rect)

    def _draw_game_over(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.assets.img_game_over, (175, 90))
        
        pos = pygame.mouse.get_pos()
        menu_rect = pygame.Rect(250, 600, 500, 150)
        self.screen.blit(self.assets.img_menu_hover if menu_rect.collidepoint(pos) else self.assets.img_menu, menu_rect)
