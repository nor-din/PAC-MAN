from __future__ import annotations
import typing
import pygame
import random
import src.game


def get_greedy_move(
        ghost: Ghost,
        maze: Maze,
        target_row: int,
        target_col: int,
        run_away: bool = False) -> None:
    directions = []
    if maze.can_move(ghost.row, ghost.col, 'up'):
        directions.append((-1, 0))
    if maze.can_move(ghost.row, ghost.col, 'down'):
        directions.append((1, 0))
    if maze.can_move(ghost.row, ghost.col, 'left'):
        directions.append((0, -1))
    if maze.can_move(ghost.row, ghost.col, 'right'):
        directions.append((0, 1))
    if ghost.current_dir and len(directions) > 1:
        reverse_dir = (-ghost.current_dir[0], -ghost.current_dir[1])
        if reverse_dir in directions:
            directions.remove(reverse_dir)
    if not directions:
        return
    best_dir = directions[0]
    best_dist = float('-inf') if run_away else float('inf')
    for (dr, dc) in directions:
        dist = (ghost.row + dr - target_row) ** 2 + \
            (ghost.col + dc - target_col) ** 2
        if run_away:
            if dist > best_dist:
                best_dist = dist
                best_dir = (dr, dc)
        elif dist < best_dist:
            best_dist = dist
            best_dir = (dr, dc)
    ghost.row += best_dir[0]
    ghost.col += best_dir[1]
    ghost.current_dir = best_dir


def chase_red(ghost: Ghost, maze: Maze,
              player: Player) -> None:
    get_greedy_move(ghost, maze, player.row, player.col)


def chase_pink(ghost: Ghost, maze: Maze,
               player: Player) -> None:
    (dr, dc) = (0, 0)
    if player.direction == 'up':
        dr = -4
    elif player.direction == 'down':
        dr = 4
    elif player.direction == 'left':
        dc = -4
    elif player.direction == 'right':
        dc = 4
    get_greedy_move(ghost, maze, player.row + dr, player.col + dc)


def chase_yellow(ghost: Ghost, maze: Maze,
                 player: Player) -> None:
    dist = (ghost.row - player.row) ** 2 + (ghost.col - player.col) ** 2
    if dist > 64:
        get_greedy_move(ghost, maze, player.row, player.col)
    else:
        get_greedy_move(ghost, maze, player.row, player.col, run_away=True)


def chase_blue(ghost: Ghost, maze: Maze,
               player: Player) -> None:
    if Ghost.red_ghost is None:
        get_greedy_move(ghost, maze, player.row, player.col)
        return

    target_row = player.row
    target_col = player.col
    if player.direction == 'up':
        target_row -= 2
    elif player.direction == 'down':
        target_row += 2
    elif player.direction == 'left':
        target_col -= 2
    elif player.direction == 'right':
        target_col += 2

    vector_row = target_row - Ghost.red_ghost.row
    vector_col = target_col - Ghost.red_ghost.col

    inky_target_row = Ghost.red_ghost.row + 2 * vector_row
    inky_target_col = Ghost.red_ghost.col + 2 * vector_col

    get_greedy_move(ghost, maze, inky_target_row, inky_target_col)


class Ghost:
    shared_mode = 'scatter'
    red_ghost: typing.Optional[Ghost] = None
    last_mode_switch_time = 0

    @classmethod
    def update_shared_mode(
            cls: type[Ghost],
            current_time: int,
            level: int = 1) -> None:
        elapsed = current_time - cls.last_mode_switch_time
        base_scatter = src.game.Game.config.scatter_duration_ms
        scatter_duration = max(1000, base_scatter - (level - 1) * 500)
        chase_duration = src.game.Game.config.chase_duration_ms
        if cls.shared_mode == 'scatter' and elapsed > scatter_duration:
            cls.shared_mode = 'chase'
            cls.last_mode_switch_time = current_time
        elif cls.shared_mode == 'chase' and elapsed > chase_duration:
            cls.shared_mode = 'scatter'
            cls.last_mode_switch_time = current_time

    def __init__(self, row: int, col: int, img_path: str,
                 chasing_function: typing.Callable[
                     [Ghost, Maze, Player],
                     None] = chase_blue) -> None:
        self.row = row
        self.col = col
        self.home = (row, col)
        self.visual_x: float = col * 40.0
        self.visual_y: float = row * 40.0
        self.is_edible = False
        self.is_eaten = False
        self.respawn_at = 0
        self.current_dir: tuple[int, int] | None = None
        self.chasing_function = chasing_function
        self.normal_img = pygame.transform.scale(
            pygame.image.load(img_path), (40, 40))
        self.edible_img = pygame.transform.scale(
            pygame.image.load('assets/images/ghost_eatble.png'), (40, 40))
        self.current_img = self.normal_img

    def update_visual(self) -> None:
        target_x = self.col * 40
        target_y = self.row * 40
        base_ticks = src.game.Game.config.ghost_speed_ticks
        current_ticks = int(
            base_ticks *
            1.25) if self.is_edible else base_ticks
        speed = 40 / current_ticks
        if self.visual_x < target_x:
            self.visual_x = min(target_x, self.visual_x + speed)
        elif self.visual_x > target_x:
            self.visual_x = max(target_x, self.visual_x - speed)
        if self.visual_y < target_y:
            self.visual_y = min(target_y, self.visual_y + speed)
        elif self.visual_y > target_y:
            self.visual_y = max(target_y, self.visual_y - speed)

    def respawn(self) -> None:
        (self.row, self.col) = self.home
        self.visual_x = self.col * 40
        self.visual_y = self.row * 40
        self.is_eaten = False
        self.is_edible = False
        self.current_dir = None

    def _move_randomly(self, maze: Maze) -> None:
        directions = []
        if maze.can_move(self.row, self.col, 'up'):
            directions.append((-1, 0))
        if maze.can_move(self.row, self.col, 'down'):
            directions.append((1, 0))
        if maze.can_move(self.row, self.col, 'left'):
            directions.append((0, -1))
        if maze.can_move(self.row, self.col, 'right'):
            directions.append((0, 1))
        if self.current_dir and len(directions) > 1:
            reverse_dir = (-self.current_dir[0], -self.current_dir[1])
            if reverse_dir in directions:
                directions.remove(reverse_dir)
        if directions:
            (dr, dc) = random.choice(directions)
            self.row += dr
            self.col += dc
            self.current_dir = (dr, dc)

    def workflow(
            self,
            maze: Maze,
            player: Player) -> None:
        if self.is_edible:
            get_greedy_move(self, maze, player.row, player.col, run_away=True)
        elif Ghost.shared_mode == 'scatter':
            self._move_randomly(maze)
        elif Ghost.shared_mode == 'chase':
            self.chasing_function(self, maze, player)

    def draw(self, screen: pygame.Surface, edible: bool = False) -> None:
        if self.is_eaten:
            return
        x = self.visual_x + 200
        y = self.visual_y + 200
        img = self.edible_img if edible else self.current_img
        screen.blit(img, (x, y))
