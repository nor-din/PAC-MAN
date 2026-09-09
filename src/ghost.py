import pygame
import random
import src.game

def get_greedy_move(ghost, maze, target_row, target_col, run_away=False):
    directions = []
    if maze.can_move(ghost.row, ghost.col, "up"): directions.append((-1, 0))
    if maze.can_move(ghost.row, ghost.col, "down"): directions.append((1, 0))
    if maze.can_move(ghost.row, ghost.col, "left"): directions.append((0, -1))
    if maze.can_move(ghost.row, ghost.col, "right"): directions.append((0, 1))
    
    # Pac-Man rule: Ghosts cannot reverse direction unless it's a dead end
    if ghost.current_dir and len(directions) > 1:
        reverse_dir = (-ghost.current_dir[0], -ghost.current_dir[1])
        if reverse_dir in directions:
            directions.remove(reverse_dir)
            
    if not directions:
        return
        
    best_dir = directions[0]
    best_dist = float('-inf') if run_away else float('inf')
    
    for dr, dc in directions:
        dist = (ghost.row + dr - target_row)**2 + (ghost.col + dc - target_col)**2
        if run_away:
            if dist > best_dist:
                best_dist = dist
                best_dir = (dr, dc)
        else:
            if dist < best_dist:
                best_dist = dist
                best_dir = (dr, dc)
                
    ghost.row += best_dir[0]
    ghost.col += best_dir[1]
    ghost.current_dir = best_dir

def chase_red(ghost, maze, player):
    # Aggressively targets player
    get_greedy_move(ghost, maze, player.row, player.col)

def chase_pink(ghost, maze, player):
    # Targets ahead of the player (ambush)
    dr, dc = 0, 0
    if player.direction == "up": dr = -4
    elif player.direction == "down": dr = 4
    elif player.direction == "left": dc = -4
    elif player.direction == "right": dc = 4
    get_greedy_move(ghost, maze, player.row + dr, player.col + dc)

def chase_yellow(ghost, maze, player):
    # Chases if far, runs away if close
    dist = (ghost.row - player.row)**2 + (ghost.col - player.col)**2
    if dist > 64: # 8 tiles
        get_greedy_move(ghost, maze, player.row, player.col)
    else:
        get_greedy_move(ghost, maze, player.row, player.col, run_away=True)

def chase_blue(ghost, maze, player):
    # Unpredictable random movement
    ghost._move_randomly(maze)

class Ghost:
    shared_mode = "scatter"
    last_mode_switch_time = 0

    @classmethod
    def update_shared_mode(cls, current_time, level=1):
        elapsed = current_time - cls.last_mode_switch_time
        base_scatter = src.game.Game.config_dict.get("scatter_duration_ms", 7000)
        # Decrease scatter duration by 500ms per level, minimum 1000ms
        scatter_duration = max(1000, base_scatter - (level - 1) * 500)
        
        chase_duration = src.game.Game.config_dict.get("chase_duration_ms", 20000)
        
        if cls.shared_mode == "scatter" and elapsed > scatter_duration:
            cls.shared_mode = "chase"
            cls.last_mode_switch_time = current_time
        elif cls.shared_mode == "chase" and elapsed > chase_duration:
            cls.shared_mode = "scatter"
            cls.last_mode_switch_time = current_time

    def __init__(self, row, col, img_path, chasing_function=None):
        self.row = row
        self.col = col
        self.home = (row, col)
        self.visual_x = col * 40
        self.visual_y = row * 40
        self.is_edible = False
        self.is_eaten = False
        self.respawn_at = 0
        self.current_dir = None
        
        # Unique chasing attribute, defaults to moving randomly
        self.chasing_function = chasing_function if chasing_function else lambda g, m, p: g._move_randomly(m)
        
        self.normal_img = pygame.transform.scale(
            pygame.image.load(img_path), (40, 40)
        )
        self.edible_img = pygame.transform.scale(
            pygame.image.load("assets/images/ghost_eatble.png"), (40, 40)
        )
        self.current_img = self.normal_img

    def update_visual(self):
        target_x = self.col * 40
        target_y = self.row * 40
        speed = 40 / src.game.Game.config_dict["ghost_speed_ticks"]
        
        if self.visual_x < target_x:
            self.visual_x = min(target_x, self.visual_x + speed)
        elif self.visual_x > target_x:
            self.visual_x = max(target_x, self.visual_x - speed)
            
        if self.visual_y < target_y:
            self.visual_y = min(target_y, self.visual_y + speed)
        elif self.visual_y > target_y:
            self.visual_y = max(target_y, self.visual_y - speed)

    def make_edible(self):
        self.is_edible = True

    def respawn(self):
        self.row, self.col = self.home
        self.visual_x = self.col * 40
        self.visual_y = self.row * 40
        self.is_eaten = False
        self.is_edible = False
        self.current_dir = None

    def _move_randomly(self, maze):
        directions = []
        if maze.can_move(self.row, self.col, "up"):
            directions.append((-1, 0))
        if maze.can_move(self.row, self.col, "down"):
            directions.append((1, 0))
        if maze.can_move(self.row, self.col, "left"):
            directions.append((0, -1))
        if maze.can_move(self.row, self.col, "right"):
            directions.append((0, 1))
            
        if self.current_dir and len(directions) > 1:
            reverse_dir = (-self.current_dir[0], -self.current_dir[1])
            if reverse_dir in directions:
                directions.remove(reverse_dir)
                
        if directions:
            dr, dc = random.choice(directions)
            self.row += dr
            self.col += dc
            self.current_dir = (dr, dc)

    def _scatter(self, maze):
        # Shared scatter method, defaults to random movement for now
        self._move_randomly(maze)

    def workflow(self, maze, player):
        if self.is_edible:
            self._move_randomly(maze)
        elif Ghost.shared_mode == "scatter":
            self._scatter(maze)
        elif Ghost.shared_mode == "chase":
            self.chasing_function(self, maze, player)

    def draw(self, screen, edible=False):
        if self.is_eaten:
            return
        x = self.visual_x + 200
        y = self.visual_y + 200
        img = self.edible_img if edible else self.current_img
        screen.blit(img, (x, y))
    