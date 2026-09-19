"""Module defining the Ghost entities, AI behaviors, and pathfinding."""
import pygame
import random
import src.game
from typing import Callable

from src.maze import Maze
from src.player import Player


def get_greedy_move(
        ghost: 'Ghost',
        maze: Maze,
        target_row: int,
        target_col: int,
        run_away: bool = False) -> None:
    """Calculates the next optimal step for a ghost.

    Args:
        ghost: The ghost entity to move.
        maze: The maze layout.
        target_row: The target row to reach or flee from.
        target_col: The target column to reach or flee from.
        run_away: If True, maximizes distance instead of minimizing it.

    Returns:
        None.
    """
    directions = ghost.valid_directions(maze)

    best_dir = directions[0]
    best_dist = float('-inf') if run_away else float('inf')
    for (dr, dc) in directions:
        d_row = ghost.row + dr - target_row
        d_col = ghost.col + dc - target_col
        dist = d_row ** 2 + d_col ** 2
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


def chase_red(ghost: 'Ghost', maze: Maze, player: Player) -> None:
    """Chase behavior for Blinky (Red Ghost).

    Targets the player's exact current grid position directly.

    Args:
        ghost: The ghost.
        maze: The maze.
        player: The player.

    Returns:
        None.
    """
    get_greedy_move(ghost, maze, player.row, player.col)


def chase_pink(ghost: 'Ghost', maze: Maze, player: Player) -> None:
    """Chase behavior for Pinky (Pink Ghost).

    Targets 4 tiles ahead to ambush.

    Args:
        ghost: The ghost.
        maze: The maze.
        player: The player.

    Returns:
        None.
    """
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


def chase_yellow(ghost: 'Ghost', maze: Maze, player: Player) -> None:
    """Chase behavior for Clyde (Yellow Ghost).

    Chases if > 8 tiles away, else flees.

    Args:
        ghost: The ghost.
        maze: The maze.
        player: The player.

    Returns:
        None.
    """
    dist = (ghost.row - player.row) ** 2 + (ghost.col - player.col) ** 2
    if dist > 64:
        get_greedy_move(ghost, maze, player.row, player.col)
    else:
        get_greedy_move(ghost, maze, player.row, player.col, run_away=True)


def chase_blue(ghost: 'Ghost', maze: Maze, player: Player) -> None:
    in_line_of_sight = (ghost.row == player.row) or (ghost.col == player.col)
    too_close = (ghost.row - player.row) ** 2 + \
                (ghost.col - player.col) ** 2 < 64

    if in_line_of_sight and too_close:
        get_greedy_move(ghost, maze, player.row, player.col)
    else:
        directions = ghost.valid_directions(maze)
        if directions:
            (dr, dc) = random.choice(directions)
            ghost.row += dr
            ghost.col += dc
            ghost.current_dir = (dr, dc)


class Ghost:
    """Represents a ghost entity in the game.

    Attributes:
        shared_mode: The global state ('scatter' or 'chase') shared by ghosts.
        last_mode_switch_time: Timestamp of the last global state change.
    """

    shared_mode = 'scatter'
    last_mode_switch_time = 0.0

    @classmethod
    def update_shared_mode(
            cls,
            current_time: float,
            level: int = 1) -> None:
        """Updates the global scatter/chase mode based on timing.

        Args:
            current_time: The current timestamp in seconds.
            level: The current game level, which shortens scatter durations.

        Returns:
            None.
        """
        current_time *= 1000
        elapsed = current_time - cls.last_mode_switch_time
        base_scatter = src.game.Game.config.scatter_duration_ms
        scatter_duration = max(4.0, base_scatter - (level - 1) * 0.5)
        chase_duration = src.game.Game.config.chase_duration_ms

        if cls.shared_mode == 'scatter' and elapsed > scatter_duration:
            cls.shared_mode = 'chase'
            cls.last_mode_switch_time = current_time

        elif cls.shared_mode == 'chase' and elapsed > chase_duration:
            cls.shared_mode = 'scatter'
            cls.last_mode_switch_time = current_time

    def __init__(self, row: int, col: int, img_path: str,
                 chasing_function: Callable[
                     ['Ghost', Maze, Player],
                     None] = chase_blue) -> None:
        """Initializes a ghost.

        Args:
            row: Starting grid row.
            col: Starting grid column.
            img_path: Path to the ghost's sprite.
            chasing_function: The specific targeting logic this ghost uses.

        Returns:
            None.
        """
        self.row = row
        self.col = col
        self.home = (row, col)
        self.visual_x: float = col * 40.0
        self.visual_y: float = row * 40.0
        self.is_edible = False
        self.is_eaten = False
        self.respawn_at = 0.0
        self.current_dir: tuple[int, int] | None = None
        self.chasing_function = chasing_function
        self.normal_img = pygame.transform.scale(
            pygame.image.load(img_path), (40, 40))
        self.edible_img = pygame.transform.scale(
            pygame.image.load('assets/images/ghost_eatble.png'), (40, 40))
        self.current_img = self.normal_img

    def valid_directions(self, maze: Maze) -> list[tuple[int, int]]:
        """Returns a list of valid moves from the current position.

        Args:
            maze: The game maze.

        Returns:
            A list of valid (dr, dc) tuples.
        """
        directions: list[tuple[int, int]] = []

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

        return directions

    def update_visual(self) -> None:
        """Smoothly interpolates the ghost's visual pixel position.

        Moves visual x/y closer to logical coordinates.

        Args:
            self: The instance object.

        Returns:
            None.
        """
        target_x = self.col * 40
        target_y = self.row * 40

        base_ticks = src.game.Game.config.ghost_speed_ticks
        if self.is_edible:
            current_ticks = int(base_ticks * 1.25)
        else:
            current_ticks = base_ticks
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
        """Resets the ghost to its home corner.

        Args:
            self: The instance object.

        Returns:
            None.
        """
        (self.row, self.col) = self.home
        self.visual_x = self.col * 40
        self.visual_y = self.row * 40
        self.is_eaten = False
        self.is_edible = False
        self.current_dir = None

    def move_randomly(self, maze: Maze) -> None:
        """Selects a random valid direction to move in the maze.

        Used primarily during the scatter phase when patrolling.

        Args:
            maze: The maze to check validity.

        Returns:
            None.
        """

    def workflow(
            self,
            maze: Maze,
            player: Player) -> None:
        """Determines the ghost's next move based on its current state.

        Executes state logic.

        Args:
            maze: The maze.
            player: The player.

        Returns:
            None.
        """
        if self.is_edible:
            get_greedy_move(self, maze, player.row, player.col, run_away=True)
        elif Ghost.shared_mode == 'scatter':
            get_greedy_move(self, maze, player.row, player.col, run_away=True)
        elif Ghost.shared_mode == 'chase':
            self.chasing_function(self, maze, player)

    def draw(self, screen: pygame.Surface, edible: bool = False) -> None:
        """Renders the ghost onto the screen.

        Args:
            screen: The Pygame surface to draw onto.
            edible: If True, draws the frightened blue sprite.

        Returns:
            None.
        """
        if self.is_eaten:
            return
        x = self.visual_x + 200
        y = self.visual_y + 200
        img = self.edible_img if edible else self.current_img
        screen.blit(img, (x, y))
