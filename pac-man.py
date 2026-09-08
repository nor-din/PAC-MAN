import pygame
import sys
from src.game_config import parse_config

def main() -> None:
    if len(sys.argv) != 2:
        raise FileNotFoundError("Missing config-file name: python3 pac-man.py config.json")
        
    config_file = sys.argv[1]
    config = parse_config(config_file)
    
    from src.game import Game
    Game.config_dict = config
    pygame.init()

    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("PAC-MAN")
    g = Game(screen)
    g.run()

    pygame.quit()


if __name__ == "__main__":
    # try:
        main()
    # except BaseException:
    #     print("Exiting program...")

