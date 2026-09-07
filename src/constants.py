from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    INSTRUCTIONS = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()

# Display Settings
FPS = 60
MAX_BOARD_WIDTH = 600
MAX_BOARD_HEIGHT = 700

# Visual Settings
LERP_FACTOR = 0.3  # Between 0.0 and 1.0 (1.0 = instant snap, 0.1 = very slow glide)

# Gameplay Logic (Lower is faster because it represents frame modulo)
PLAYER_MOVE_TICK = 6
GHOST_MOVE_TICK = 12
RESPAWN_DELAY_MS = 8000
EDIBLE_DURATION_MS = 7000

# Scoring
POINTS_PACGUM = 10
POINTS_SUPER_PACGUM = 50
POINTS_GHOST = 200
