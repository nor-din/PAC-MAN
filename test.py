import pygame
from moviepy import VideoFileClip

pygame.init()

screen = pygame.display.set_mode((800, 450))
pygame.display.set_caption("MP4 Test")

video = VideoFileClip("test.mp4")

clock = pygame.time.Clock()

for frame in video.iter_frames(fps=1, dtype="uint8"):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            video.close()
            exit()

    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    frame_surface = pygame.transform.scale(frame_surface, (800, 450))

    screen.blit(frame_surface, (0, 0))
    pygame.display.flip()

    clock.tick(30)

video.close()
pygame.quit()
