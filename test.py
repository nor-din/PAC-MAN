import pygame
pygame.init()


surface = pygame.Surface((100, 100))
surface.fill((0, 0, 0))
font = pygame.font.Font(None, 50)
text = font.render("START", True, (255, 255, 255))
surface.blit(text, (0, 0))
pygame.image.save(surface, f"assets/images/start.png")

print("Digits created!")