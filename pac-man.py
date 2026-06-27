import pygame
from src.game import Game


pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("PAC-MAN")
g = Game(screen)
g.run()

pygame.quit()