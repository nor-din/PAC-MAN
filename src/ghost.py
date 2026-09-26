"""Module defining the Ghost entities, AI behaviors, and pathfinding."""
import time
import pygame
import random
import src.game

from src.maze import Maze
from src.player import Player


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
        """Update the global scatter/chase mode based on timing.

        Args:
            current_time: The current timestamp in seconds.
            level: The current game level, which shortens scatter durations.

        Returns:
            None.
        """
        current_time *= 1000
        elapsed = current_time - cls.last_mode_switch_time
        base_scatter = src.game.Game.config.scatter_duration_ms
        scatter_duration = max(4000.0, base_scatter - (level - 1) * 500.0)
        chase_duration = src.game.Game.config.chase_duration_ms

        if cls.shared_mode == 'scatter' and elapsed > scatter_duration:
            cls.shared_mode = 'chase'
            cls.last_mode_switch_time = current_time

        elif cls.shared_mode == 'chase' and elapsed > chase_duration:
            cls.shared_mode = 'scatter'
            cls.last_mode_switch_time = current_time

    def __init__(self, row: int, col: int, img_path: str) -> None:
        """Initialize a ghost.

        Args:
            row: Starting grid row.
            col: Starting grid column.
            img_path: Path to the ghost's sprite.

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
        Ghost.last_mode_switch_time = time.time() * 1000
        self.current_dir: tuple[int, int] | None = None
        self.normal_img = pygame.transform.scale(
            pygame.image.load(img_path), (40, 40))
        self.edible_img = pygame.transform.scale(
            pygame.image.load('assets/images/ghost_eatble.png'), (40, 40))
        self.current_img = self.normal_img

    def valid_directions(self, maze: Maze) -> list[tuple[int, int]]:
        """Return a list of valid moves from the current position.

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
        """Reset the ghost to its home corner.

        Returns:
            None.
        """
        (self.row, self.col) = self.home
        self.visual_x = self.col * 40
        self.visual_y = self.row * 40
        self.is_eaten = False
        self.is_edible = False
        self.current_dir = None

    def chase(self, maze: Maze, player: Player) -> None:
        """Define the chasing behavior. To be overridden by subclasses.

        Args:
            maze: The current maze.
            player: The player object to chase.

        Returns:
            None.
        """
        self.move_randomly(maze)

    def move_randomly(self, maze: Maze) -> None:
        """Move the ghost in a random valid direction.

        Args:
            maze: The current maze object.

        Returns:
            None.
        """
        directions = self.valid_directions(maze)

        if not directions:
            return

        if len(directions) > 1 and self.current_dir is not None:
            rev_row = self.current_dir[0] * -1
            rev_col = self.current_dir[1] * -1

            if (rev_row, rev_col) in directions:
                directions.remove((rev_row, rev_col))

        random_dr, random_dc = random.choice(directions)
        self.row += random_dr
        self.col += random_dc
        self.current_dir = (random_dr, random_dc)

    def get_greedy_move(
            self,
            maze: Maze,
            target_row: int,
            target_col: int,
            run_away: bool = False) -> None:
        """Calculate the next optimal step for a ghost.

        Args:
            maze: The maze layout.
            target_row: The target row to reach or flee from.
            target_col: The target column to reach or flee from.
            run_away: If True, maximizes distance instead of minimizing it.

        Returns:
            None.
        """
        directions = self.valid_directions(maze)

        best_dir = directions[0]
        best_dist = float('-inf') if run_away else float('inf')

        for (dr, dc) in directions:
            d_row = self.row + dr - target_row
            d_col = self.col + dc - target_col
            dist = d_row ** 2 + d_col ** 2
            if run_away:
                if dist > best_dist:
                    best_dist = dist
                    best_dir = (dr, dc)
            elif dist < best_dist:
                best_dist = dist
                best_dir = (dr, dc)

        self.row += best_dir[0]
        self.col += best_dir[1]
        self.current_dir = best_dir

    def workflow(
            self,
            maze: Maze,
            player: Player) -> None:
        """Determine the ghost's next move based on its current state.

        Executes state logic.

        Args:
            maze: The maze.
            player: The player.

        Returns:
            None.
        """
        if self.is_edible:
            self.get_greedy_move(maze, player.row, player.col, run_away=True)

        elif Ghost.shared_mode == 'scatter':
            self.move_randomly(maze)

        elif Ghost.shared_mode == 'chase':
            self.chase(maze, player)

    def draw(self, screen: pygame.Surface, edible: bool = False) -> None:
        """Render the ghost onto the screen.

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


class RedGhost(Ghost):
    """Blinky (Red Ghost)."""

    def __init__(self, row: int, col: int) -> None:
        """Initialize the red ghost.

        Args:
            row: Starting row.
            col: Starting col.
        """
        super().__init__(row, col, "./assets/images/ghost_red.png")

    def chase(self, maze: Maze, player: Player) -> None:
        """Chase the player using a greedy approach.

        Args:
            maze: The current maze.
            player: The player object to chase.

        Returns:
            None.
        """
        self.get_greedy_move(maze, player.row, player.col)


class PinkGhost(Ghost):
    """Pinky (Pink Ghost)."""

    def __init__(self, row: int, col: int) -> None:
        """Initialize the pink ghost.

        Args:
            row: Starting row.
            col: Starting col.
        """
        super().__init__(row, col, "./assets/images/ghost_pink.png")

    def chase(self, maze: Maze, player: Player) -> None:
        """Chase a target slightly ahead of the player.

        Args:
            maze: The current maze.
            player: The player object to chase.

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

        self.get_greedy_move(maze, player.row + dr, player.col + dc)


class YellowGhost(Ghost):
    """Clyde (Yellow Ghost)."""

    def __init__(self, row: int, col: int) -> None:
        """Initialize the yellow ghost.

        Args:
            row: Starting row.
            col: Starting col.
        """
        super().__init__(row, col, "./assets/images/ghost_yellow.png")

    def chase(self, maze: Maze, player: Player) -> None:
        """Chase the player or run away based on distance.

        Args:
            maze: The current maze.
            player: The player object to chase.

        Returns:
            None.
        """
        run_away = True
        dist = (self.row - player.row) ** 2 + (self.col - player.col) ** 2

        if dist > 64:
            run_away = False

        self.get_greedy_move(maze, player.row, player.col, run_away=run_away)


class BlueGhost(Ghost):
    """Inky (Blue Ghost)."""

    def __init__(self, row: int, col: int) -> None:
        """Initialize the blue ghost.

        Args:
            row: Starting row.
            col: Starting col.
        """
        super().__init__(row, col, "./assets/images/ghost_blue.png")
