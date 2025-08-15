import pygame
from time import sleep
import numpy as np


def show_picture(screen, path):
    # Load the image
    image = pygame.image.load(path)

    # Scale to fill the screen
    image = pygame.transform.scale(image, screen.get_size())

    # Grayscale
    arr = pygame.surfarray.array3d(image)  # shape: (width, height, 3)
    gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)
    gray_rgb = np.stack([gray] * 3, axis=-1)
    gray_surface = pygame.surfarray.make_surface(gray_rgb.swapaxes(0, 1))

    gray_surface = pygame.transform.rotate(gray_surface, -90)
    gray_surface = pygame.transform.flip(gray_surface, True, False)

    # Draw on screen
    screen.blit(gray_surface, (0, 0))
    pygame.display.flip()
    sleep(1)