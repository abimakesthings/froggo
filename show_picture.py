import pygame
from time import sleep


def show_picture(screen, path):
    # Load the image
    image = pygame.image.load(path)

    # Scale to fill the screen
    image = pygame.transform.scale(image, screen.get_size())

    # Draw on screen
    screen.blit(image, (0, 0))
    pygame.display.flip()
    sleep(1)