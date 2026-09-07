import sys
import pygame
from src.game import Game
from src.config import load_config

def main() -> None:
    # Check if config was provided
    if len(sys.argv) < 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)
        
    config = load_config(sys.argv[1])
        
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("PAC-MAN")
    
    g = Game(screen)
    # Inject config settings (You can expand this later)
    g.max_time = config.get("level_max_time", 90)
    g.run()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        # Re-raise during development, or sys.exit(1) in production
        raise
