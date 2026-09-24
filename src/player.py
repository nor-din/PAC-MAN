"""Module managing the Player entity, movement and visual interpolation."""
import pygame
import src.game


class Player:
    """Represents the Pac-Man player entity."""

    def __init__(self, row: int, col: int) -> None:
        """Initialize the player.

        Args:
            row: Starting grid row.
            col: Starting grid column.

        Returns:
            None.
        """
        self.row = row
        self.col = col
        self.visual_x: float = col * 40.0
        self.visual_y: float = row * 40.0

        self.lives = src.game.Game.config.lives
        self.score = 0

        self.direction = 'right'
        self.counter = 0
        self.index = 0
        self.invincible = False

    def update_visual(self, speed_multiplier: float) -> None:
        """Smoothly interpolates the player's visual pixel position.

        Args:
            speed_multiplier: Modifies movement speed for visual snapping.

        Returns:
            None.
        """
        target_x = self.col * 40
        target_y = self.row * 40

        speed = 40 / src.game.Game.config.player_speed_ticks * speed_multiplier

        if self.visual_x < target_x:
            self.visual_x = min(target_x, self.visual_x + speed)
        elif self.visual_x > target_x:
            self.visual_x = max(target_x, self.visual_x - speed)
        if self.visual_y < target_y:
            self.visual_y = min(target_y, self.visual_y + speed)
        elif self.visual_y > target_y:
            self.visual_y = max(target_y, self.visual_y - speed)

    def teleport(self, row: int, col: int) -> None:
        """Instantly moves the player to a new grid location.

        Args:
            row: New logical row.
            col: New logical column.

        Returns:
            None.
        """
        self.row = row
        self.col = col
        self.visual_x = col * 40
        self.visual_y = row * 40

    def move_right(self, maze: src.maze.Maze) -> None:
        """Attempt to move the player right.

        Args:
            maze: The maze to check for wall collisions.

        Returns:
            None.
        """
        if maze.can_move(self.row, self.col, 'right'):
            self.col += 1
            self.direction = 'right'

    def move_left(self, maze: src.maze.Maze) -> None:
        """Attempt to move the player left.

        Args:
            maze: The maze to check for wall collisions.

        Returns:
            None.
        """
        if maze.can_move(self.row, self.col, 'left'):
            self.col -= 1
            self.direction = 'left'

    def move_up(self, maze: src.maze.Maze) -> None:
        """Attempt to move the player up.

        Args:
            maze: The maze to check for wall collisions.

        Returns:
            None.
        """
        if maze.can_move(self.row, self.col, 'up'):
            self.row -= 1
            self.direction = 'up'

    def move_down(self, maze: src.maze.Maze) -> None:
        """Attempt to move the player down.

        Args:
            maze: The maze to check for wall collisions.

        Returns:
            None.
        """
        if maze.can_move(self.row, self.col, 'down'):
            self.row += 1
            self.direction = 'down'

    def draw(self, screen: pygame.Surface) -> None:
        """Render the player onto the screen based on their current direction.

        Args:
            screen: The Pygame surface to draw onto.

        Returns:
            None.
        """
        anim_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f'assets/images/pac_man_open_{self.direction}.png'),
                (36, 36)),
            pygame.transform.scale(
                pygame.image.load('assets/images/pac_man_close.png'),
                (36, 36))
            ]

        inv_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f'assets/images/pac_man_open_'
                    f'{self.direction}_invincible.png'),
                (36, 36)),
            pygame.transform.scale(
                pygame.image.load(
                    'assets/images/pac_man_close_invincible.png'),
                (36, 36))
            ]
        self.counter += 1
        if self.counter >= 12:
            self.counter = 0
            self.index += 1
        if self.invincible:
            frame = inv_frames[self.index % len(inv_frames)]
        if not self.invincible:
            frame = anim_frames[self.index % len(anim_frames)]
        x = self.visual_x + 200 + (40 - 36) // 2
        y = self.visual_y + 200 + (40 - 36) // 2
        screen.blit(frame, (x, y))
