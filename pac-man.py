import pygame
from src.player import Player

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)

maze = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

# Create player
player = Player(row=1, col=1)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left(maze)
    if keys[pygame.K_RIGHT]:
        player.move_right(maze)
    if keys[pygame.K_UP]:
        player.move_up(maze)
    if keys[pygame.K_DOWN]:
        player.move_down(maze)

    # Draw
    screen.fill(BLACK)

    # Draw maze
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 1:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (c * 40, r * 40, 40, 40)
                )

    # Draw player
    player.draw(screen)

    # Draw score + lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(
        f"Score: {player.score}",
        True,
        (255, 255, 255)
    )
    lives_text = font.render(
        f"Lives: {player.lives}",
        True,
        (255, 255, 255)
    )
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (200, 10))

    pygame.display.update()

pygame.quit()