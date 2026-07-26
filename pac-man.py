import pygame
from src.game import Game


pygame.init()

screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("PAC-MAN")
g = Game(screen)
g.run()

pygame.quit()