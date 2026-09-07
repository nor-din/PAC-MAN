import pygame


class AssetManager:
    """Manages all game assets (images), loading them once from disk and caching them."""

    def __init__(self) -> None:
        # UI Images (pre-scaled)
        self.img_title = pygame.transform.scale(pygame.image.load("assets/images/title.png"), (550, 150))
        self.img_start = pygame.transform.scale(pygame.image.load("assets/images/start.png"), (400, 150))
        self.img_start_hover = pygame.transform.scale(pygame.image.load("assets/images/start_hover.png"), (400, 150))
        self.img_highscore = pygame.transform.scale(pygame.image.load("assets/images/highscore.png"), (400, 150))
        self.img_highscore_hover = pygame.transform.scale(
            pygame.image.load("assets/images/highscore_hover.png"), (400, 150))
        self.img_instructions = pygame.transform.scale(pygame.image.load("assets/images/instructions.png"), (400, 150))
        self.img_instructions_hover = pygame.transform.scale(
            pygame.image.load("assets/images/instructions_hover.png"), (400, 150))
        self.img_exit = pygame.transform.scale(pygame.image.load("assets/images/exit.png"), (400, 150))
        self.img_exit_hover = pygame.transform.scale(pygame.image.load("assets/images/exit_hover.png"), (400, 150))

        self.img_dig = {}
        for d in "0123456789":
            self.img_dig[d] = pygame.transform.scale(pygame.image.load(f"assets/images/digit_{d}.png"), (40, 40))

        self.img_heart = pygame.transform.scale(pygame.image.load("assets/images/heart.png"), (50, 50))
        self.img_game_over = pygame.transform.scale(pygame.image.load("assets/images/game_over.png"), (650, 400))
        self.img_menu = pygame.transform.scale(pygame.image.load("assets/images/menu.png"), (500, 150))
        self.img_menu_hover = pygame.transform.scale(pygame.image.load("assets/images/menu_hover.png"), (500, 150))
        self.img_pause = pygame.transform.scale(pygame.image.load("assets/images/pause.png"), (100, 100))
        self.img_pause_title = pygame.transform.scale(pygame.image.load("assets/images/pause_title.png"), (800, 400))
        self.img_continue = pygame.transform.scale(pygame.image.load("assets/images/continue.png"), (500, 150))
        self.img_continue_hover = pygame.transform.scale(
            pygame.image.load("assets/images/continue_hover.png"), (500, 150))
        self.img_on = pygame.transform.scale(pygame.image.load("assets/images/on.png"), (100, 50))
        self.img_off = pygame.transform.scale(pygame.image.load("assets/images/off.png"), (100, 50))
        self.img_freeze = pygame.transform.scale(pygame.image.load("assets/images/freeze.png"), (250, 70))
        self.img_invincible = pygame.transform.scale(pygame.image.load("assets/images/invincible.png"), (200, 50))
        self.img_speed = pygame.transform.scale(pygame.image.load("assets/images/speed.png"), (250, 70))
        self.img_instructions_title = pygame.transform.scale(
            pygame.image.load("assets/images/instructions_title.png"), (800, 200))
        self.img_controls = pygame.transform.scale(pygame.image.load("assets/images/controls.png"), (700, 500))
        self.img_box = pygame.image.load("assets/images/box.png")
        self.img_box = pygame.transform.scale(self.img_box, (500, 150))
        # Raw Game Entity Images (Unscaled)
        self._raw_ghosts = {
            "pink": pygame.image.load("assets/images/ghost_pink.png"),
            "green": pygame.image.load("assets/images/ghost_green.png"),
            "yellow": pygame.image.load("assets/images/ghost_yellow.png"),
            "blue": pygame.image.load("assets/images/ghost_blue.png"),
            "edible": pygame.image.load("assets/images/ghost_eatble.png"),
        }

        self._raw_player = {
            "close": pygame.image.load("assets/images/pac_man_close.png"),
            "close_invincible": pygame.image.load("assets/images/pac_man_close_invincible.png"),
            "open_up": pygame.image.load("assets/images/pac_man_open_up.png"),
            "open_down": pygame.image.load("assets/images/pac_man_open_down.png"),
            "open_left": pygame.image.load("assets/images/pac_man_open_left.png"),
            "open_right": pygame.image.load("assets/images/pac_man_open_right.png"),
            "open_invincible_up": pygame.image.load("assets/images/pac_man_open_up_invincible.png"),
            "open_invincible_down": pygame.image.load("assets/images/pac_man_open_down_invincible.png"),
            "open_invincible_left": pygame.image.load("assets/images/pac_man_open_left_invincible.png"),
            "open_invincible_right": pygame.image.load("assets/images/pac_man_open_right_invincible.png")
        }

        self._raw_maze = {
            "wall_h": pygame.image.load("assets/images/wall_h.png"),
            "wall_v": pygame.image.load("assets/images/wall_v.png")
        }

        self._raw_pacgum = {
            "normal": pygame.image.load("assets/images/pacgum.png"),
            "super": pygame.image.load("assets/images/super_pacgum.png")
        }

        # Caches for scaled images
        self.ghosts: dict[str, pygame.Surface] = {}
        self.player: dict[str, pygame.Surface] = {}
        self.maze: dict[str, pygame.Surface] = {}
        self.pacgum: dict[str, pygame.Surface] = {}

    def scale_level_assets(self, cell_size: int) -> None:
        """Scales all raw images to fit the current cell_size exactly once per level."""
        for k, img in self._raw_ghosts.items():
            self.ghosts[k] = pygame.transform.scale(img, (cell_size, cell_size))

        # Player is typically slightly smaller than the full cell to avoid clipping visually
        p_size = int(cell_size * 0.9)
        for k, img in self._raw_player.items():
            self.player[k] = pygame.transform.scale(img, (p_size, p_size))

        wall_thick = max(1, cell_size // 10)
        self.maze["wall_h"] = pygame.transform.scale(self._raw_maze["wall_h"], (cell_size, wall_thick))
        self.maze["wall_v"] = pygame.transform.scale(self._raw_maze["wall_v"], (wall_thick, cell_size))

        pacgum_size = int(cell_size * 0.5)
        self.pacgum["normal"] = pygame.transform.scale(self._raw_pacgum["normal"], (pacgum_size, pacgum_size))
        self.pacgum["super"] = pygame.transform.scale(self._raw_pacgum["super"], (pacgum_size, pacgum_size))
