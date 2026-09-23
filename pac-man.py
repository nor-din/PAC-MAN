"""Entry point for the PAC-MAN game.

Handles config loading, Pygame initialization, and launches the game loop.
"""
import pygame
import sys
from src.game import Game
from src.game_config import GameConfig


def main() -> None:
    """Entry point for the application.

    Parses command-line arguments, loads the configuration, initializes Pygame,
    and starts the main game loop.

    Args:
        None.

    Returns:
        None.
    """
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.json'):
        print(
            'Error: Missing config-file name.'
            'Usage: python3 pac-man.py <config.json>',
            file=sys.stderr)
        sys.exit(1)

    config_file: str = sys.argv[1]
    config = GameConfig.parse_config(config_file)
    Game.config = config

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('PAC-MAN')
    g = Game(screen)
    g.run()
    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGame interrupted (Ctrl+C). Exiting...', file=sys.stderr)
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f'\nFatal Error: {e}', file=sys.stderr)
        pygame.quit()
        sys.exit(1)
