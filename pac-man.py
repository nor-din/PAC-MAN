import pygame

pygame.init()

pacman_imgs = [
    "./assets/images/pacman_up.png",
    "./assets/images/pacman_right.png",
    "./assets/images/pacman_down.png",
    "./assets/images/pacman_left.png"
]

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH = screen.get_width()
HEIGHT = screen.get_height()

BLACK = (0, 0, 0)
BLUE  = (0, 0, 255)

images = {
    "up":    pygame.transform.scale(
                pygame.image.load(pacman_imgs[0]), (40, 40)),
    "right": pygame.transform.scale(
                pygame.image.load(pacman_imgs[1]), (40, 40)),
    "down":  pygame.transform.scale(
                pygame.image.load(pacman_imgs[2]), (40, 40)),
    "left":  pygame.transform.scale(
                pygame.image.load(pacman_imgs[3]), (40, 40)),
}

background = pygame.image.load("./assets/images/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

CELL_SIZE = 50
maze = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

row = 1
col = 1
direction = "right"
current_img = images["right"]

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if maze[row][col - 1] == 0:
            col -= 1
        direction = "left"
        current_img = images["left"]

    if keys[pygame.K_RIGHT]:
        if maze[row][col + 1] == 0:
            col += 1
        direction = "right"
        current_img = images["right"]

    if keys[pygame.K_UP]:
        if maze[row - 1][col] == 0:
            row -= 1
        direction = "up"
        current_img = images["up"]

    if keys[pygame.K_DOWN]:
        if maze[row + 1][col] == 0:
            row += 1
        direction = "down"
        current_img = images["down"]

    screen.blit(background, (0, 0))

    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 1:
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    screen.blit(
        current_img,
        (col * CELL_SIZE, row * CELL_SIZE)
    )

    pygame.display.update()

pygame.quit()