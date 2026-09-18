"""Module for loading graphical assets and rendering UI components."""
import sys
import pygame


class Images:
    """Preloads and stores all visual assets for the UI and backgrounds."""

    def __init__(self) -> None:
        """Loads background, menu, and UI images from the assets folder.

        Args:
            self: The instance object.

        Returns:
            None.
        """
        try:
            self.img_title = pygame.image.load('assets/images/title.png')
            self.img_start = pygame.image.load('assets/images/start.png')
            self.img_start_hover = pygame.image.load(
                'assets/images/start_hover.png')
            self.img_highscore = pygame.image.load(
                'assets/images/highscore.png')
            self.img_highscore_hover = pygame.image.load(
                'assets/images/highscore_hover.png')
            self.img_instructions = pygame.image.load(
                'assets/images/instructions.png')
            self.img_instructions_hover = pygame.image.load(
                'assets/images/instructions_hover.png')
            self.img_exit = pygame.image.load('assets/images/exit.png')
            self.img_exit_hover = pygame.image.load(
                'assets/images/exit_hover.png')
            self.img_heart = pygame.image.load('assets/images/heart.png')
            self.img_game_over = pygame.image.load(
                'assets/images/game_over.png')
            self.img_menu = pygame.image.load('assets/images/menu.png')
            self.img_menu_hover = pygame.image.load(
                'assets/images/menu_hover.png')
            self.img_pause = pygame.image.load('assets/images/pause.png')
            self.img_pause_title = pygame.image.load(
                'assets/images/pause_title.png')
            self.img_continue = pygame.image.load('assets/images/continue.png')
            self.img_continue_hover = pygame.image.load(
                'assets/images/continue_hover.png')
            self.img_on = pygame.image.load('assets/images/on.png')
            self.img_off = pygame.image.load('assets/images/off.png')
            self.img_freeze = pygame.image.load('assets/images/freeze.png')
            self.img_invincible = pygame.image.load(
                'assets/images/invincible.png')
            self.img_speed = pygame.image.load('assets/images/speed.png')
            self.img_instructions_title = pygame.image.load(
                'assets/images/instructions_title.png')
            self.img_highscore_title = pygame.image.load(
                'assets/images/highscore_title.png')
            self.img_controls = pygame.image.load('assets/images/controls.png')
            self.img_box = pygame.image.load('assets/images/box.png')
            self.img_save = pygame.image.load('assets/images/save.png')
            self.img_save_hover = pygame.image.load(
                'assets/images/save_hover.png')
            self.img_victory = pygame.image.load('assets/images/victory.png')
            self.img_background = pygame.image.load(
                'assets/images/background.png')
            self.img_rules = pygame.image.load('assets/images/rules.png')
        except FileNotFoundError:
            print('Image not Found', file=sys.stderr)
            sys.exit(1)
