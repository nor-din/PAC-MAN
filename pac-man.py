import pygame
from src.game import Game



def main() -> None:
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

